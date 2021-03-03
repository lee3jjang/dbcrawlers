set ie = createobject("internetexplorer.application")

ie.navigate "http://vm10.dbins.co.kr"
ie.visible = true

do while ie.busy = true
    wscript.sleep 500
loop

ie.document.all.item("userId").value = "사번"
ie.document.all.item("userPwd").value = "비번"
ie.document.all.item("login_form_submit").click