import { useHookstate } from "@hookstate/core";
import { _currentMailbox, _currentMailboxEmails, _currentUser, _isSettingsOpen } from "../App";
import { getEmails } from "../api/GmailImap";
import { AuthorizedUser } from "../classes/AuthorizedUser";
import EvaButton from "../particle-component/EvaButton";

// const inboxNavButtonStyle = 
// `flex justify-center items-center group
//   bg-gradient-to-br from-teal-600 to-teal-300  text-white w-full h-14 p-1
//   shadow-slate-800 shadow-lg
//   hover:text-blue-700 hover:scale-90 hover:shadow-none hover:from-teal-400 hover:to-teal-100
//   focus:text-blue-700 focus:scale-90 focus:shadow-none focus:bg-gray-100
//   transition-all duration-200`

const inboxNavButtonStyle = 
`flex justify-center items-center group
  bg-white text-gray-600 w-full h-14 p-1
  hover:shadow-inner hover:shadow-black hover:bg-gray-100
  focus:shadow-inner focus:shadow-black focus:bg-gray-100
  transition-all duration-200`

function onClick(folder: string, user: AuthorizedUser){
  if(folder === 'Settings'){
    _isSettingsOpen.set(true)
    console.log('SETTINGS CLICKED')
    console.log("THIS SETTINGS THINGS: " + _isSettingsOpen.get())
  }else if(folder === 'Eva'){
    console.log('EVA CLICKED')
    // sendEmail(user.email, user.access_token);
  }else{
    localStorage.setItem('currentMailbox', folder);
    _currentMailbox.set(folder)
    _currentMailboxEmails.set(localStorage.getItem(folder) || '')
    console.log("GETTING CURRENT EMAILS: " + localStorage.getItem(folder))
    console.log("OTHER" + folder)
    getEmails(folder)
  }
}

function onHover(folder: string, user: AuthorizedUser){
  if(folder === 'Eva'){
    console.log('EVA CLICKED')
    // sendEmail(user.email, user.access_token);
  }
}

function InboxNavButton(props: {folder: string, label: string; primaryIcon: string, secondaryIcon?: string}) {
  const currentUser = useHookstate(_currentUser);
  const user: AuthorizedUser = currentUser.get()
  // console.log("InboxNavButton USER EMAIL:", user.email)
  let rounded = ' hover:rounded-3xl focus:rounded-3xl rounded-xl'
  if(props.label == 'Eva'){
    rounded = ' rounded-full'
  }
  return (
    <>
      <li className="px-3 pb-1 pt-2">
        <a href={"#" + props.label}>
          <div className="group">
            {/* Help tabs */}
            {/* <div className={"fixed z-50 left-16 pt-2 scale-0 group-hover:scale-100 transition-all duration-50"}>
              <div className=" text-white bg-slate-800 rounded-lg p-1">
                {props.label}
              </div>
            </div> */}
            <button className={inboxNavButtonStyle + rounded} onClick={() => onClick(props.folder!, user)} onMouseEnter={() => onHover(props.folder!, user)}>
              <img src={props.primaryIcon}/>
              {/* <img className="" src={props.secondaryIcon}/> */}
            </button>
          </div>
        </a>
      </li>
    </>
  )
}
  
export default InboxNavButton
