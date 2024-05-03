// import { _selectedEmail } from "../App";
import { getEmail } from "../api/GmailImap"

const emailListItemStyle = 
`flex justify-between
  rounded-lg w-210 p-5
  text-blue-700 bg-gray-100
  border-b border-blue-700
  hover:bg-gray-300`

async function onEmailClick(uid: string){
  // window.scrollTo({ top: 0, behavior: "smooth" })
  // localStorage.setItem('selectedEmail', html);
  // _selectedEmail.set(html);

  console.log("EMAIL UID: " + uid)
  const result = await getEmail(uid)

}

function formatDate(dateString: string){
  const now = new Date()
  // console.log("NOW: " + now.getFullYear)
  const date = new Date(dateString);
  let dateFormat = date.getMonth() + 1 + '/' + date.getUTCDate() + '/' + date.getFullYear() + ' ' + date.getHours() + ':' + date.getMinutes()
  // console.log("DATEFORMAT: " + dateFormat)
  return dateFormat
}

function EmailListItem(props: {email: any}) {
  // const email = JSON.parse(props.email);
  const email = props.email
  // const date = new Date(email['date']);
  const date = formatDate(email['date'])
  // console.log("EMAIL 1234567: " + email)
  return (
    <>
      <li key={email.uid}>
        <button className={emailListItemStyle} onClick={() => onEmailClick(email['uid'])}>
        {/* <div className="columns-1 grow"> */}
          <div>{email['from']}</div>
          <div>{email['subject']}</div>
          <div>{date}</div>
          {/* {email['from']}
          {email['to']}
          {email['data']}
          {email['attachments']} */}
        {/* </div> */}
        </button>
      </li>
    </>
  )
}

export default EmailListItem
