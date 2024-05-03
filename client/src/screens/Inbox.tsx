import { useHookstate } from "@hookstate/core";
import { _isComposeOpen, _selectedEmail } from "../App";
import Email from "../components/Email"
import EmailList from "../components/EmailList"
import InboxNav from "../components/InboxNav"
import InboxOptionsBar from "../components/InboxOptionsBar";
import SettingsModal from "../components/SettingsModal";

function Inbox() {
  const selectedEmail = useHookstate(_selectedEmail);
  const isComposeOpen = useHookstate(_isComposeOpen);
  let style = "columns-1 grow gap-0";
  let composeStyle = " left-20";
  const last = _selectedEmail.get()
  // console.log("LAST VALUE: " + last)
  if(selectedEmail.get() != ''){
    style = "columns-2 grow gap-0";
  }if(isComposeOpen.get() == true){
    composeStyle = " left-[50%]"
    style = "columns-2 width-[50%] gap-0"
  }if(selectedEmail.get() != last){
    _isComposeOpen.set(false)
  }


  return (
    <>
      <div className="flex bg-gradient-to-t from-gray-950 to-gray-800">
        <InboxNav/>
        <div className={"fixed flex-row box-border w-full transition-all duration-200" + composeStyle}>
          <InboxOptionsBar/>
          <div className={style}>
            <EmailList/>
            <Email/>
          </div>
        </div>
      </div>
      <SettingsModal/>
    </>
  )
}
  
export default Inbox
