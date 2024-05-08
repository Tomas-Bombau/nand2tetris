const {instructionAtoBinary, instructionCtoBinary, instructionToVariable, instructionForLabel} = require("./Code")


const Parser = (file, symbols) => {
    const instructions = []
    console.log(file)
    file.forEach(element => {
        if(element.startsWith("@") && /\d/.test(element.charAt(1))){
            console.log(element)
            const binaryCodeA = instructionAtoBinary(element)
            instructions.push(binaryCodeA)
        }

        else if(element.startsWith("@") && /[a-zA-Z]/.test(element.charAt(1))){
            const label = element.split("@")
            const labelName = label[1]
            const binaryVariable = instructionToVariable(symbols[labelName])
            instructions.push(binaryVariable)
        }

        else if(element.startsWith("(")){
            let label = element.substring(1, element.length - 1)
            const binaryCodeLabel = instructionForLabel(symbols[label])
            instructions.push(binaryCodeLabel)
        }

        else{
            const binaryCodeC = instructionCtoBinary(element)
            instructions.push(binaryCodeC)
        }
    })

    console.log(instructions)
    return instructions
}

module.exports = Parser
