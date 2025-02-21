const crypto = require('crypto');
  
let messageJson = {};
messageJson.amount = "1.00"; //utilizar punto para el separador de decimales
messageJson.payerID = "V18184460"; //la letra el inicio del numero de identificacion debe ser mayúscula
messageJson.payerPhone = "04244445566"; //el número telefonico debe iniciar en 0
messageJson.tokenOtp = "01452454"; //token Otp en formato String
messageJson.order = "ABC123"; // Identificador unico de la operación

const encryptedMessage = encryptDataTransaction(JSON.stringify(messageJson));
const decryptedMessage = decryptDataTransaction(encryptedMessage);
console.log('Mensaje original:', decryptedMessage);
console.log('Mensaje encriptado:', encryptedMessage);

function encryptDataTransaction(message) {
    const key = Buffer.from([78, 41, 78, 31, 44, 63, 121, 80, 41, 27, 113, 0, 3, 64, 27, 2, 78, 58, 78, 78, 44, 63, 96, 102]);
    const iv = Buffer.from([122, 23, 98, 32, 67, 32, 86, 57]);
    const cipher = crypto.createCipheriv('des-ede3-cbc', key, iv);
    let encrypted = cipher.update(message, 'utf-8', 'base64');
    encrypted += cipher.final('base64');
    return encrypted;
}

function decryptDataTransaction(encryptedMessage) {
    const key = Buffer.from([78, 41, 78, 31, 44, 63, 121, 80, 41, 27, 113, 0, 3, 64, 27, 2, 78, 58, 78, 78, 44, 63, 96, 102]);
    const iv = Buffer.from([122, 23, 98, 32, 67, 32, 86, 57]);
    const decipher = crypto.createDecipheriv('des-ede3-cbc', key, iv);
    let decrypted = decipher.update(encryptedMessage, 'base64', 'utf-8');
    decrypted += decipher.final('utf-8');
    return decrypted;
}

