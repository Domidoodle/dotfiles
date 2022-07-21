import sys;
import os;
import time as t;
import subprocess;
import json

# subprocess wrapper
# returns stdout with weird shell business removed
def run(args, stdin=None):
    program = subprocess.run(args, capture_output=True, text=True, stdin=stdin);
    return program.stdout;

def bar(fraction):
    bar = subprocess.Popen(["gdbar", "-max", "1"], text=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE);
    stdout = bar.communicate(input=str(fraction))[0];
    return str(stdout.replace("\n", ""));


def dawk(string, searchLine, column=None):
    for line in string.split("\n"):
        if searchLine in line:
            if column != None:
                item = ((line.split(" "))[column]);
            else:
                item = line;
            return item;


def common():
    # datetime
    # date = run(["date", "+%e %b"]);
    # time = run(["date", "+%H:%M"]);
    # moment = run(["/home/domidoodle/devel/hextime/clock"]);

     # music
    music = run(["playerctl", "-p", "ncspot,spotify,firefox", "metadata", "--format", "{{ artist }}: {{ title }} [{{ playerName }}]"]);
    if music == "": music = "No Media";

    # focused window
    xprop = run(["xprop", "-root"]);
    id = dawk(xprop, "_NET_ACTIVE_WINDOW", -1);
    xprop = run(["xprop", "-id", id]);
    print(dawk(xprop, "_NET_WM_NAME"));
    try:
        # program name only
        windowFocused = dawk(xprop, "_NET_WM_NAME", -1).replace("\"", "");
        # full title
    except:
        windowFocused = "";

    # ram
    meminfo = open("/proc/meminfo", "r");
    meminfo = meminfo.read();
    memtotal = int(dawk(meminfo, "MemTotal", -2));
    memfree = int(dawk(meminfo, "MemFree", -2));
    memcached = int(dawk(meminfo, "Cached", -2));
    membuffers = int(dawk(meminfo, "Buffers", -2));
    memused = (memtotal - memfree - memcached - membuffers);
    membar = bar(memused / memtotal);
    memunused = memtotal - memused;

    # cpu
    cpuinfo = open("/proc/stat", "r");
    cpuinfo = cpuinfo.readline();
    cpuinfo = cpuinfo.split(" ")[2:-2];
    for i in range(len(cpuinfo)):
        cpuinfo[i] = int(cpuinfo[i]);
    # 0 user
    # 1 nice
    # 2 system
    # 3 idle
    # 4 iowait
    # 5 irq
    # 6 softirq
    # 7 steal
    cpuIdle = cpuinfo[3] + cpuinfo[4];
    cpuNonIdle = cpuinfo[0] + cpuinfo[1] + cpuinfo[2] + cpuinfo[5] + cpuinfo[6] + cpuinfo[7];
    cpuTotal = cpuIdle + cpuNonIdle;

    cpuTotalLast = 0;
    cpuIdleLast = 0;

    # im lazy
    cpuTotald = cpuTotal - cpuTotalLast;
    cpuIdled = cpuIdle - cpuIdleLast;
    cpuusage = (cpuTotald - cpuIdled) / cpuTotald;

    cpuTotalLast = cpuTotal;
    cpuIdleLast = cpuIdle;

    # apkg
    apkg = len(run(["checkupdates"]).split("\n"));

    # datetime but implemented in python which seems to use 0.7% cpu at peak
    # put it at the end incase that makes it faster for some reason
    ss70 = t.time();
    tm = t.localtime();
    if tm.tm_isdst == 1:
        tz = t.timezone + 3600;
    else:
        tz = t.timezone;
    
    ssm = int(ss70 + tz) % 86400;
    lag = 1;
    mosm = int(ssm * 0.54 + lag); 
    moment = "";
    i = 0;
    while mosm // 6**i != 0:
        moment = str(mosm // 6**i % 6) + moment[::1];
        i += 1;

    datetime = t.localtime();
    time = t.strftime("%H:%M");
    date = t.strftime("%e %b")


    return "{centre}{space} {windowFocused} {space}{right}{space} {music} {space} {fg[11]}{date}{fg[5]} {space} {fg[11]}{time}{fg[5]} {space} {fg[9]}{moment}{fg[5]} {space}"\
.format(centre=center, windowFocused=windowFocused, music=music, date=date, time=time, moment=moment, colour=colour, space=space, fg=fg, bg=bg, left=left, center=center, right=right).replace("\n", "");

def main():

    displays = []; #display[0] displays port, display[1] resolutionX, resolutionY, x, y
    xrandr = run(["xrandr"]);
    for line in xrandr.split("\n"):
        if " connected " in line:
            columns = line.split(" ");
            display = [];
            display.append(columns[0]);
            display.append(columns[2].replace("x", "+").split("+"));
            displays.append(display);

    for display in displays:
        instances = [];
        instances.append(subprocess.Popen(["lemonbar", "-p", "-g", "{}x{}+{}+{}".format(display[1][0], 15, display[1][2], 0),
                                "-B", str("#" + bgalpha + colour[0][1::]), "-F", str(colour[5]),
                                "-f", font
                                ], text=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE));
        display.append(instances);

    print(displays);

    # don't think there is anyway for a workspace to be focused and not visible
    workspaceStates = [" {workspace} ", # none 
                       "{bg[2]}|{workspace}|{bg[0]}", # visible
                       "", # focused - never used?
                       "{bg[3]}[{workspace}]{bg[0]}", # visible & focused 
                       "{bg[8]}!{workspace}!{bg[0]}", # urgent
                       "{bg[8]}!{workspace}!{bg[0]}", # visible & urgent
                       "", # focused & urgent - never used?
                       "{bg[8]}!{workspace}!{bg[0]}"]; # visible & focused & urgent

    while True:
        commonStatus = common();
        print(commonStatus);
        i3info = run(["i3-msg", "-t", "get_workspaces"]);
        try:
            workspaces = json.loads(i3info);
        except:
            pass
        for display in displays:
            displayStatus = left; # displayed on left side
            # i3
            for workspace in workspaces:
                if workspace["output"] == display[0]:
                    # visible, focused, urgent
                    workspacestate = 0;
                    if workspace["visible"]: workspacestate |= 1;
                    if workspace["focused"]: workspacestate |= 2;
                    if workspace["urgent"]: workspacestate |= 4;
                    displayStatus += space + workspaceStates[workspacestate].format(workspace=workspace["name"], fg=fg, bg=bg);
            displayStatus += space;
            
            # write 
            display[2][0].stdin.flush();
            display[2][0].stdin.write(displayStatus + commonStatus + "\n");
        t.sleep(0.5 / 0.54);


if __name__ == "__main__":
    # colors
    colour = [
        "#282828",
        "#3c3836",
        "#504945",
        "#665c54",
        "#bdae93",
        "#d5c4a1",
        "#ebdbb2",
        "#fbf1c7",
        "#fb4934",
        "#fe8019",
        "#fabd2f",
        "#b8bb26",
        "#8ec07c",
        "#83a598",
        "#d3869b",
        "#d65d0e"
    ];

    bgalpha = "aa";

    fg = ["%{F" + col + "}" for col in colour];
    bg = ["%{B#" + bgalpha + col[1::] + "}" for col in colour];

    space = "{fg[3]}|{fg[5]}".format(fg=fg);

    left = "%{l}";
    center = "%{c}";
    right = "%{r}";

    font = "ubuntu mono:size=11";

    main();
