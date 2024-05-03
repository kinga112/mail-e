import GoogleAuthButton from '../components/GoogleAuthButton';
import EvaButton from '../particle-component/EvaButton';

function Login() {
  return (
    <> 
      <div className='flex flex-row justify-center items-center p-20 font-thin text-5xl'>Mail - E</div>
      <div className='flex flex-row justify-center items-center p-5'>
        <div className='min-w-96 min-h-80 bg-white border rounded-lg shadow-xl'>
          <div className='flex justify-center pt-20'>
            <GoogleAuthButton/>
            {/* <EvaButton/> */}
          </div>
        </div>
      </div>
    </>
  )
}
  
export default Login
