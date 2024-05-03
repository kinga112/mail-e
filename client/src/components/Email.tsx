import ReactHtmlParser from 'html-react-parser'; 
import { _selectedEmail } from '../App';
import { useHookstate } from '@hookstate/core';

function Email() {
  const selectedEmail = useHookstate(_selectedEmail);

  return (
    <>
      <div className="sticky h-screen overflow-y-scroll overscroll-contain bg-gray-100">
        <div className="pt-16">
          { ReactHtmlParser(selectedEmail.get()) }
        </div>
      </div>
    </>
  )
}
  
export default Email
