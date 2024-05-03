import { _selectedEmail } from "../App";

const inboxNavButtonStyle = 
`bg-gray-100 h-8 text-black rounded-lg p-1 border border-teal-400 
  hover:shadow-none hover:bg-gray-100 hover:bg-gray-300`

  function onButtonClick(button: string){
  if(button == 'close'){
    localStorage.setItem('selectedEmail', '')
    _selectedEmail.set('')
  }
}

function InboxOptionBarButton(props: {label?: string; icon?: string, onClick?: string}) {
  return (
    <>
      <li className="px-3 py-2">
        <button className={inboxNavButtonStyle} onClick={() => onButtonClick(props.onClick!)}>
            {props.label}
            <img src={props.icon}/>
        </button>
      </li>
    </>
  )
}
  
export default InboxOptionBarButton
