import { useHookstate } from "@hookstate/core";
import { _currentMailboxEmails } from "../App";
import EmailListItem from "./EmailListItem";

function EmailList() {
  const currentMailboxEmails = useHookstate(_currentMailboxEmails);

  let emailListItems = [];
  if(currentMailboxEmails.get() == ''){
    console.log("Could not load email list")
  }
  else if(currentMailboxEmails.get() != '{}'){
    const getEmails = JSON.parse(currentMailboxEmails.get())
    // using any as email type because unknown JSON object coming from backend
    emailListItems = getEmails.map((email: any) => <EmailListItem email={email}/>);
  }else{
    console.log("currentMailboxEmails STATE: ", currentMailboxEmails.get())
  }

  return (
    <>
      <div className="sticky h-screen overflow-y-scroll overscroll-contain bg-gray-500 grow rounded-l-4xl">
        <div className="p-5 pt-16">
          <ul>{emailListItems}</ul>
        </div>
      </div>
    </>
  )
}

export default EmailList
