import { hookstate, useHookstate } from '@hookstate/core';
import Cookies from 'universal-cookie';
import Inbox from './screens/Inbox';
import Login from './screens/Login';
import { AuthorizedUser } from './classes/AuthorizedUser';

// initialize global states
// I moved to hookstate library to call states at top level, I found this easiest with global states
export const cookies = new Cookies(null, { path: '/' });
export const _currentMailboxEmails = hookstate<string>('');
export const _currentMailbox = hookstate<string>('');
export const _selectedEmail = hookstate<string>('');
export const _authorized = hookstate<boolean>(false);
export const _currentUser = hookstate<AuthorizedUser>(new AuthorizedUser('', '', 0, ''));
export const _isSettingsOpen = hookstate<boolean>(false);
export const _isComposeOpen = hookstate<boolean>(false);

// Point Eel web socket to the instance
export const eel = window.eel
eel.set_host( 'ws://localhost:8888' )

function checkLocalStorage(){
  // _currentMailboxEmails.set('')
  // _selectedEmail.set('')
  console.log("CHECKING COOKIES: " + cookies.get('authorized'));
  if(cookies.get('authorized') == true){
    _authorized.set(true);
    // _authorized.set(false)
    // cookies.set('authorized', false)
  }

  const currentUser = localStorage.getItem('currentUser') || '{}';
  console.log("CURRENT USER::" + currentUser);
  console.log("CURRENT USER 2::" + JSON.stringify(currentUser));
  if(currentUser != '{}'){
    const currentAuthUser = JSON.parse(currentUser)
    console.log("USER AUTH USER TOKEN:" + currentAuthUser['access_token'])
    const authUser = new AuthorizedUser(currentAuthUser['email'], 
                                        currentAuthUser['access_token'], 
                                        currentAuthUser['expires_in'], 
                                        currentAuthUser['refresh_token'])
    _currentUser.set(authUser);
  }
  
  const currentMailboxEmails = localStorage.getItem(localStorage.getItem('currentMailbox') || '') || '{}';
  _currentMailboxEmails.set(currentMailboxEmails);
  // console.log("SETTING SELECTED EMAIL")
  const selectedEmail = localStorage.getItem('selectedEmail') || '';
  // console.log("GOT: " + selectedEmail)
  if(selectedEmail != ''){
    // console.log("SELECTED EMAIL: " + selectedEmail)
    _selectedEmail.set(selectedEmail);
  }
}

function App() {
  <><script src="particle-image.js"></script><script src="particle-image.min.js"></script></>
  const authorized = useHookstate(_authorized);
  console.log("AUTHORIZE STATE: ", authorized.get())
  checkLocalStorage();
  return (
    authorized.get() ? <Inbox/> : <Login/>
    // <Inbox/>
  );
}

export default App;
