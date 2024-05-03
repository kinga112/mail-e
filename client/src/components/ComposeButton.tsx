import { hookstate, useHookstate } from "@hookstate/core";
import { _currentUser, _isComposeOpen, _isSettingsOpen } from "../App";
import compose from "../assets/icons/compose.svg"
import { motion } from "framer-motion";
import closeIcon from '../assets/icons/close.svg';
import loadingIcon from '../assets/icons/loading.svg';
import sendIcon from '../assets/icons/sent.svg';
import { sendEmail } from "../api/GmailImap";
import { AuthorizedUser } from "../classes/AuthorizedUser";

const composeButtonStyle = 
` flex justify-center items-center group
bg-gradient-to-br from-teal-300 to-teal-50  text-white w-full h-14 p-2
shadow-black rounded-2xl hover:text-blue-700 hover:scale-110
transition-all duration-200`

const exitButtonStyle = 
`float-right z-10 w-10 h-10 bg-blue-600 mr-5
  shadow-lg shadow-gray-500 text-white
  content-center rounded-full items-center justify-center
  hover:shadow-none hover:bg-red-600
  transition-all duration-100`

const sendButtonStyle = 
`absolute bottom-5 right-10 z-10 h-16 mr-5 text-white
  content-center rounded-full items-center justify-center
  transition-all duration-100`

const _loading = hookstate<boolean>(false);
const _to = hookstate<string>('');
const _subject = hookstate<string>('');
const _body = hookstate<string>('');

async function sendOnClick(user: AuthorizedUser, to: string, subject: string, body: string){
  _loading.set(true)
  await sendEmail(user.email, user.access_token, to, subject, body)
  _to.set('')
  _subject.set('')
  _body.set('')
  _loading.set(false)
}

function ComposeWindow(){
  const to = useHookstate(_to);
  const subject = useHookstate(_subject);
  const body = useHookstate(_body);
  const loading = useHookstate(_loading);
  const currentUser = useHookstate(_currentUser);
  const user: AuthorizedUser = currentUser.get()
  
  let colorStyle =
  ` w-24 shadow-lg shadow-gray-500 text-black bg-blue-600
    hover:shadow-none hover:bg-gray-300 hover:text-blue-600`

  if(loading.get()){
    colorStyle = ' bg-gray-300 w-16'
  }
  
  return (
      <>
        <div className="fixed w-[46%] h-[97%] bottom-5 left-24">
          <button className={exitButtonStyle} onClick={() => _isComposeOpen.set(false)}>
            <div className="scale-75">
              <img className="pl-2" src={closeIcon}/>
            </div>
          </button>
          <button className={sendButtonStyle + colorStyle} onClick={() => sendOnClick(user, to.get(), subject.get(), body.get())}>
            <div className="scale-75">
              {loading.get() ? <div className="p-1 animate-spin"><img src={loadingIcon}/></div> : <div className="p-2 flex">Send<img className="ml-2" src={sendIcon}/></div> }
            </div>
          </button>
          <div className="mt-12 flex flex-col gap-2 w-full h-[95%]">
            <input className="w-[95%] h-10 px-2 rounded-md text-black" value={to.get()} type="text" placeholder=" To: " id="to" onChange={ e => {_to.set(e.target.value)} }/>
            <input className="w-[95%] h-10 px-2 rounded-md text-black" value={subject.get()}  type="text" placeholder=" Subject: " id="subject" onChange={ e => {_subject.set(e.target.value)} }/>
            <textarea id="message" className="w-[95%] h-full p-2 rounded-md resize-none text-black" value={body.get()} onChange={ e => {_body.set(e.target.value)} }/>
          </div>
        </div>
      </>
  )
}

function composeOnClick(){
  _isComposeOpen.set(true)
}

function ComposeButton() {
//   const currentUser = useHookstate(_currentUser);
//   const user: AuthorizedUser = currentUser.get()
//   console.log("InboxNavButton USER EMAIL:", user.email)
  const label = 'Compose'
  return (
    <>
      <ComposeWindow/>
      <li className="px-3 pb-1 pt-2">
        <a href={"#" + label}>
          <div className="group">
            {/* <div className={"fixed z-50 left-16 pt-2 scale-0 group-hover:scale-100 transition-all duration-50"}>
              <div className=" text-white bg-slate-800 rounded-lg p-1">
                {label}
              </div>
            </div> */}
            <button className={composeButtonStyle} onClick={() => composeOnClick()}>
              <img src={compose}/>
              {/* <img className="" src={props.secondaryIcon}/> */}
            </button>
          </div>
        </a>
      </li>
    </>
  )
}
  
export default ComposeButton
