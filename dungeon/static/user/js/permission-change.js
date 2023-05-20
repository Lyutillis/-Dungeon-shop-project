var updateChecks = document.getElementsByClassName('check-superuser')
var action = null

for(i = 0; i < updateChecks.length; i++){
	updateChecks[i].addEventListener('change', function(){
        var userId = this.dataset.user
        if (this.checked){
            action = 'True'
            updateUserPermissions(userId, action, 'superuser')
        }	 else {
            action = 'False'
            updateUserPermissions(userId, action, 'superuser') 
        }
    })
}

updateChecks = document.getElementsByClassName('check-staff')

for(i = 0; i < updateChecks.length; i++){
	updateChecks[i].addEventListener('change', function(){
        var userId = this.dataset.user
        if (this.checked){
            action = 'True'
            updateUserPermissions(userId, action, 'staff')
        }	 else {
            action = 'False'
            updateUserPermissions(userId, action, 'staff') 
        }
    })
}

function updateUserPermissions(userId, action, type){
		if (type=='superuser') {
            var url = '/update-permission-superuser/'
        } else {
            var url = '/update-permission-staff/'
        }

		fetch(url, {
			method: 'POST',
			headers:{
				'Content-Type':'application/json',
				'X-CSRFToken': csrftoken,
			},
			body:JSON.stringify({'userId': userId, 'action': action})
		})

	.then((response) => {
		return response.json();
	})

	.then((data) => {
		location.reload()
	});
}