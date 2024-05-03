import { _authorized, _currentUser, eel } from '../App';
import { cookies } from '../App';
import { AuthorizedUser } from '../classes/AuthorizedUser';
import CLIENT_ID from '../config';

async function onClick(){
  const response_type = 'code';
  const scope = 'https://www.googleapis.com/auth/userinfo.email%20https://mail.google.com/';
  const client_id = CLIENT_ID;
  // const redirect_uri = 'http://localhost:5000';
  const redirect_uri = 'http://localhost:3000/gmail/auth';
  const state = '';
  const authUrl = 'https://accounts.google.com/o/oauth2/auth?access_type=offline&prompt=consent&response_type=' + response_type + 
                  '&scope=' + scope + '&client_id=' + client_id + '&redirect_uri=' + redirect_uri + '&state=' + state;
  
  window.open(authUrl);
  const response = await eel.authorize('gmail')();
  const responseString = JSON.stringify(response);
  
  console.log("AUTH REQUEST STRING: " + responseString)

  const responseJson = JSON.parse(responseString)

  if(responseJson['Authenticated'] == 'True'){
      _authorized.set(true);
      cookies.set('authorized', true);
      // console.log(requestString + typeof(requestString))
      // const requestMap: Map<string, any> = new Map(Object.entries(JSON.parse(requestString)));
      // console.log("REQUEST 2: " + requestMap.get('email'))

      // const newUser = new AuthorizedUser(requestMap.get('email'), 
                                        // requestMap.get('access_token'), 
                                        // requestMap.get('expires_in'), 
                                        // requestMap.get('refresh_token'));
      // _currentUser.set(newUser);
      // localStorage.setItem('currentUser', JSON.stringify(newUser));
    }

  // if(requestString.includes('access_token')){
  //   _authorized.set(true);
  //   cookies.set('authorized', true);
  //   console.log(requestString + typeof(requestString))
  //   const requestMap: Map<string, any> = new Map(Object.entries(JSON.parse(requestString)));
  //   console.log("REQUEST 2: " + requestMap.get('email'))

  //   const newUser = new AuthorizedUser(requestMap.get('email'), 
  //                                      requestMap.get('access_token'), 
  //                                      requestMap.get('expires_in'), 
  //                                      requestMap.get('refresh_token'));
  //   _currentUser.set(newUser);
  //   localStorage.setItem('currentUser', JSON.stringify(newUser));
  // }
}

function GoogleAuthButton() {
  return (
    <>
      <button className='border border-gray-400 bg-gray-100 p-3 rounded-md hover:bg-gray-200' onClick={onClick}>
        Connect Gmail
      </button>
    </>
  )
}
  
export default GoogleAuthButton
