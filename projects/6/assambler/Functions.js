const decimalABinario = (num) => {
    let binary = []
 
    while (num !== 0) {
       var digito = num % 2
       num = Math.floor(num / 2)
       binary = digito + binary
    }
    return binary;
 
}

function convertTo16Bit(binaryString) {
    while (binaryString.length < 15) {
        binaryString = '0' + binaryString;
    }
    return binaryString;
}

module.exports = {decimalABinario, convertTo16Bit}