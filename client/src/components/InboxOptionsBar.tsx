import { useHookstate } from "@hookstate/core";
import { _isSettingsOpen, _selectedEmail } from "../App";
import InboxNavButton from "./InboxNavButton"
import InboxOptionsBarButton from "./InboxOptionsBarButton"
import reply from "../assets/icons/reply.svg"
import replyAll from "../assets/icons/reply-all.svg"
import forward from "../assets/icons/forward.svg"
import close from "../assets/icons/close.svg"
import add from "../assets/icons/add.svg"

const inboxOptionsBarStyle = 
`fixed top-3 z-10 mx-5 h-12 bg-gradient-to-br from-teal-300 to-teal-50 w-200
  shadow-md shadow-gray-500 rounded-xl`

const alignStyle = 
`flex flex-row w-full overflow-hidden`

function InboxOptionsBar() {
  const selectedEmail = useHookstate(_selectedEmail);
  const isSettingsOpen = useHookstate(_isSettingsOpen);
  let style = "columns-1 grow h-12"
  let visible = ' invisible'
  if(selectedEmail.get() != ''){
    style = "columns-2 grow h-12"
    visible = ' visible overflow-visible'
  }
  let inboxOptionsBarVisibility = ''
  if(isSettingsOpen.get() == true){
    inboxOptionsBarVisibility = ' hidden'
  }
  
  return (
    <>
      <div className={inboxOptionsBarStyle + inboxOptionsBarVisibility}>
          <ul className={style}>
            <ul className={alignStyle}>
              <div className="flex flex-row w-full">
                <InboxOptionsBarButton label="Google"/>
                <InboxOptionsBarButton label="Work"/>
                <InboxOptionsBarButton label="To Do"/>
                <InboxOptionsBarButton label="Reminders"/>
              </div>
              <div className="justify-end"><InboxOptionsBarButton icon={add}/></div>
            </ul>
            <ul className={alignStyle + visible}>
              <div className="w-1 bg-gray-700 mt-1 mb-2 rounded-lg ml-6 opacity-60"/> {/* divider */}
              <div className="flex flex-row w-full">
                <InboxOptionsBarButton icon={reply}/>
                <InboxOptionsBarButton icon={replyAll}/>
                <InboxOptionsBarButton icon={forward}/>
              </div>
              <div className="justify-end scale-110"><InboxOptionsBarButton icon={close} onClick="close"/></div>
            </ul>
          </ul>
      </div>
    </>
  )
}

export default InboxOptionsBar
