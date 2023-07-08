function sendMail(){
    var nameField = document.getElementById("name");
    var nameValue = nameField.value;

    var emailField = document.getElementById("email");
    var emailValue = emailField.value;

    var messagesField = document.getElementById("messages");
    var messagesValue = messagesField.value;
    

    
    var templateParams = {
        from_name: nameValue,
        from_email: emailValue,
        from_messages: messagesValue,
    };

    const serviceID = "gmail";
    const templateID = "Sosotech";
    
    emailjs.send(serviceID,templateID,templateParams,)
    .then(
        res =>{
            document.getElementById("name").value = "";
            document.getElementById("email").value = "";
            document.getElementById("messages").value = "";
            console.log(res);
            alert("Your message was sent successfully!");
        }
    )
    .catch((err) => console.log(err));
}


