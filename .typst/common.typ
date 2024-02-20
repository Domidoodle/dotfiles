#let conf(
	colour,
	code_colour,
	doc,
) = {

set page(
  fill: colour.at(0)
)

set text(
  font: "Ubuntu",
  fill: colour.at(5),
  size: 11pt,
)

// code
set raw(theme: "base16-gruvbox-dark-medium.tmTheme")
show raw.where(block: true): it => { 
  let x = it.text.split("\n").enumerate();
  let n = "";
  for (i, line) in x {
    let num = str(i+1);
    while num.len() < 3 {
      num = " " + num;
    }
    n += num + "\n";
  }
  let size_line = 2.5em;
  let size_code = 100% - size_line;
  grid(
    rows: 2,
    block(
  	  fill: code_colour.at(0),
      stroke: 1pt + code_colour.at(1),
      inset: 8pt,
      grid(
        columns: (size_line, size_code),
        block(
          fill: rgb(code_colour.at(0)),
          width: size_line,
          text(
            font: "Ubuntu Mono",
            fill: code_colour.at(3), 
            size: 11pt,
            n,
          )
        ),
        block(
          fill: rgb(code_colour.at(0)),
          width: size_code,
          text(
            font: "Ubuntu Mono",
            fill: code_colour.at(5), 
            size: 11pt,
            it,
          )
        )
      ),
    ),
    block(
      stroke: 1pt + code_colour.at(1),
      inset: 2pt,
      width: 100%,
      height: auto,
      fill: code_colour.at(1),
      align(
        end, 
        text(
          font: "Ubuntu Mono",
          fill: code_colour.at(4),
          size: 11pt,    
          it.lang          
        )
      )
    )
  )
}

show raw.where(block: false): it => text(
  font: "Ubuntu Mono",
  size: 11pt,
  it,
)

set table(
  stroke: none,
  fill: (col, row) => if calc.odd(row) { colour.at(2) } else { colour.at(1) },
  inset: 8pt,
)

set list(
  marker: [--]
)

show link: it => {
  set text(fill: colour.at(13));
  underline(it)
}

doc
}



