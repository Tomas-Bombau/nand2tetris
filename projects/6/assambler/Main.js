const fs = require("fs");
const addSymbols = require("./AddSymbols");
const Parser = require("./Parser");
const filePath = "./Examples/MaxL.asm";



const Main = async (file) => {
    let cleanLines = []
    let eraseLines=[]

    let contentFile = await fs.promises.readFile(file, 'utf8')
    let allLines = contentFile.split('\n')
    allLines.forEach(line => {
        if (line.trimStart().startsWith("//")) {
            eraseLines.push(line.trim());
        } else {
            cleanLines.push(line.trim());
        }
    });

    const linesToAnalyze = cleanLines.filter(line => line.trim() !== '')
    //First pass
    const symbols = addSymbols(linesToAnalyze)

    //Cleaning (XXX)
    linesToAnalyze.forEach((line, index) => {
        if(line.startsWith("(")){
            linesToAnalyze.splice(index, 1)
        }
    })
    // Parser module in action
    const binaryArray = Parser(linesToAnalyze, symbols)
}



Main(filePath)










