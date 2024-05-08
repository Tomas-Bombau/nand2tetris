const {symbols} = require("./SymbolTable");

const addSymbols = (file) => {
  const labels = [];
  const variables = [];
  let i = 16;
  let counter = 0

  file.forEach((element, index) => {
    if (element.startsWith("(")) {
      let getName = element.substring(1, element.length - 1);
      const labelSymbol = { [getName]: index - counter};
      labels.push(labelSymbol);
      Object.assign(symbols, ...labels);
      counter++
    }
  });



  file.forEach((element) => {
    if (element.startsWith("@") && /[a-zA-Z]/.test(element[1])) {
      let getNameVariable = element.substring(1, element.length);
      if (symbols.hasOwnProperty(getNameVariable)) {
        null;
      } else {
        variables.push({ [getNameVariable]: i });
        Object.assign(symbols, ...variables);
        i++;
      }
    }
  });

  
  return symbols
};

module.exports = addSymbols;
