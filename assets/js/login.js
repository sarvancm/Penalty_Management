const signUpButton = document.getElementById('signUp');
const signInButton = document.getElementById('signIn');
const container = document.getElementById('container');

signUpButton.addEventListener('click', () => {
	container.classList.add("right-panel-active");
});

signInButton.addEventListener('click', () => {
	container.classList.remove("right-panel-active");
});


// =======   Password View    ======


const pwShowHide = document.querySelectorAll(".showHidePw"),
        pwFields = document.querySelectorAll(".password"),
		pwShowHide1 = document.querySelectorAll(".showHidePw11"),
        pwFields1 = document.querySelectorAll(".password11");

          //js code to show/hide password and change icon

    pwShowHide.forEach(eyeIcon =>{
        eyeIcon.addEventListener('click',()=>{
            pwFields.forEach(pwFields =>{
                if(pwFields.type === "password"){
                    pwFields.type = "text";
                    pwShowHide.forEach(icon =>{
                        icon.classList.replace("fa-eye-slash" , "fa-eye")
                    })
                }
                else{
                    pwFields.type = "password"
                    pwShowHide.forEach(icon =>{
                        icon.classList.replace("fa-eye" , "fa-eye-slash")
                    })
                }
            })
        })
    })

	pwShowHide1.forEach(eyeIcon =>{
        eyeIcon.addEventListener('click',()=>{
            pwFields1.forEach(pwFields1 =>{
                if(pwFields1.type === "password"){
                    pwFields1.type = "text";
                    pwShowHide1.forEach(icon =>{
                        icon.classList.replace("fa-eye-slash" , "fa-eye")
                    })
                }
                else{
                    pwFields1.type = "password"
                    pwShowHide1.forEach(icon =>{
                        icon.classList.replace("fa-eye" , "fa-eye-slash")
                    })
                }
            })
        })
    })