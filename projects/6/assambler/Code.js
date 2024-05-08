const {decimalABinario, convertTo16Bit} = require("./Functions")
const {jumpTable, destTable, compTable} = require("./SymbolTable")


const instructionAtoBinary = (instructionA) => {
    const elementSplited = instructionA.split("@")
    if(elementSplited[0] == ""){elementSplited[0] = "0"}
    let bit15 = elementSplited[0]
    let numberToBinary = decimalABinario(elementSplited[1])
    let numberToBinary15bit = convertTo16Bit(numberToBinary)
    let instructionABinary = bit15 + numberToBinary15bit
    return instructionABinary
}

const instructionToVariable = (variable) => {
  let numberToBinary = decimalABinario(variable)
  let numberToBinary15bit = convertTo16Bit(numberToBinary)
  let instructionToVariable = 0 + numberToBinary15bit
  return instructionToVariable
}

const instructionForLabel = (label) => {
  let numberToBinary = decimalABinario(label)
  let numberToBinary15bit = convertTo16Bit(numberToBinary)
  let labelBinary = 0 + numberToBinary15bit
  return labelBinary
}

const instructionCtoBinary = (instructionC) => {
  let compTableBinary = "000000"
  let destTableBinary = "000"
  let jumpTableBinary = "000"
  let a = 0
  
  if(instructionC.includes("=")){
    let compAndDest = instructionC.split("=")
    let comp = compAndDest[1]
    let dest = compAndDest[0]
    if(comp == "M" || comp == "!M" || comp == "-M" || comp == "M+1" || comp == "M-1" || comp == "D+M" || comp == "D-M" || comp == "M-D" || comp == "D&M" || comp == "D|M"){
        compTableBinary = compTable[a + 1][comp]
        a++
    } else {
        compTableBinary = compTable[a][comp]
    }
    destTableBinary = destTable[dest]
  }


  if(instructionC.includes(";")){
    let jumps = instructionC.split(";")
    let comp = jumps[0]
    compTableBinary = compTable[a][comp]
    let kidnOfJump = jumps[1]
    if(kidnOfJump == "JGT" || kidnOfJump == "JEQ" || kidnOfJump == "JGE" || kidnOfJump == "JLT" || kidnOfJump == "JNE" || kidnOfJump == "JLE" || kidnOfJump == "JMP"){
      jumpTableBinary = jumpTable[kidnOfJump]
    } else{
      null
    }
  }

  return("111" + a + compTableBinary + destTableBinary + jumpTableBinary)
}

module.exports = {instructionAtoBinary, instructionCtoBinary, instructionToVariable, instructionForLabel}




//   if(instructionC.includes(";")){
//     let jumps = instructionC.split("=")

//   }