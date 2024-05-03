import InboxNavButton from "./InboxNavButton"
import inboxIcon from "../assets/icons/inbox.svg"
import inboxRefreshIcon from "../assets/icons/inboxRefresh.svg"
import important from "../assets/icons/important.svg"
import starred from "../assets/icons/starred.svg"
import drafts from "../assets/icons/drafts.svg"
import sent from "../assets/icons/sent.svg"
import spam from "../assets/icons/spam.svg"
import trash from "../assets/icons/trash.svg"
import eva from "../assets/icons/eva2.svg"
import settings from "../assets/icons/settings.svg"
import ComposeButton from "./ComposeButton"
import EvaButton from "../particle-component/EvaButton"

function InboxNav() {
  return (
    <>
      <div className="flex flex-col justify-between w-20 h-screen text-center pt-2 pb-2 text-white text-lg font-medium">
        <ul>
          {/* <div>
            MAIL&#x2022;E
          </div> */}
          <ComposeButton/>
          <InboxNavButton folder='Inbox' label='Inbox' primaryIcon={inboxIcon} secondaryIcon={inboxRefreshIcon}/>
          <InboxNavButton folder='Important' label='Important' primaryIcon={important}/>
          <InboxNavButton folder='Starred' label='Starred' primaryIcon={starred}/>
          <InboxNavButton folder='Drafts' label='Drafts' primaryIcon={drafts}/>
          <InboxNavButton folder='Sent Mail' label='Sent' primaryIcon={sent}/>
          <InboxNavButton folder='Spam' label='Spam' primaryIcon={spam}/>
          <InboxNavButton folder='Trash' label='Trash' primaryIcon={trash}/>
        </ul>
        <ul>
          <InboxNavButton folder='Eva' label='Eva' primaryIcon={eva}/>
          {/* <EvaButton/> */}
          <InboxNavButton folder='Settings' label='Settings' primaryIcon={settings}/>
        </ul>
        {/* <div className="absolute bottom-16 left-1 pb-2">
          <EvaButton/>
        </div> */}
      </div>
    </>
  )
}

export default InboxNav
