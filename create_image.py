# $language = "Python"
# $interface = "1.0"




import SecureCRT

tab=crt.GetScriptTab()

row=tab.Screen.CurrentRow
prompt=tab.Screen.Get(row,0,row,crt.Screen.CurrentColumn-1)
prompt=prompt.strip()


tab.Screen.Synchronous = True
tab.Screen.IgnoreEscape = True


def main():
	linux_sysname=["centos","ubuntu","arch","fedora","debian","coreos","openwrt","cirros"]
	img_info=crt.Dialog.Prompt("请输入要创建的镜像的操作系统名称、镜像文件格式、镜像文件路径、镜像名称（以英文逗号隔开）：")	
	img_sysname=img_info.split(",")[0]
	img_type=img_info.split(",")[1]
	img_file_path=img_info.split(",")[2]
	img_name=img_info.split(",")[3]
	tab.Screen.Send(" source  /etc/kolla/admin-openrc.sh"+"\n")
	tab.Screen.WaitForStrings(prompt,30000)
	if img_type=="iso":
		tab.Screen.Send("openstack image create --container-format bare --disk-format iso  --public --file "+img_file_path+" "+img_name+"\n")
		tab.Screen.WaitForStrings(prompt,30000)
		crt.Dialog.MessageBox("创建完成")
	else:
		if (img_sysname in linux_sysname):
			tab.Screen.Send("openstack image create --container-format bare --disk-format "+img_type+" --property hw_qemu_guest_agent=yes --property os_type=linux --property os_distro="+img_sysname+"  --public --file "+img_file_path+" "+img_name+"\n")
			tab.Screen.WaitForStrings(prompt,30000)
		if img_sysname=="windows":
			tab.Screen.Send("openstack image create --container-format bare --disk-format "+img_type+" --property hw_qemu_guest_agent=yes --property os_type=windows --property os_distro="+img_sysname+"  --property os_admin_user=Administrator --public --file "+img_file_path+" "+img_name+"\n")
			tab.Screen.WaitForStrings(prompt,30000)
		if img_sysname=="cirros":
			tab.Screen.Send("openstack image create --container-format bare --disk-format "+img_type+" --property hw_qemu_guest_agent=yes --property os_distro=others  --public --file "+img_file_path+" "+img_name+"\n")
			tab.Screen.WaitForStrings(prompt,30000)
		crt.Dialog.MessageBox("创建完成")
main()
