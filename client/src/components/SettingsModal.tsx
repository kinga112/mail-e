import Modal from 'react-modal';
import { _isSettingsOpen } from '../App';
import { useHookstate } from '@hookstate/core';
import closeIcon from '../assets/icons/close.svg';

const modalStyle = 
`bg-blue`

const exitButtonStyle = 
`float-right z-10 w-10 h-10 bg-teal-100
  shadow-lg shadow-gray-500 text-white
  content-center rounded-full items-center justify-center
  hover:shadow-none hover:bg-red-600
  transition-all duration-100`

function SettingsModal() {
  const isSettingsOpen = useHookstate(_isSettingsOpen);
  return (
    <>
      <Modal isOpen={
        isSettingsOpen.get()}
        style={{
          overlay: {
            position: 'fixed',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            backgroundColor: 'rgba(0, 0, 0, 0.9)',
          },
          content: {
            position: 'absolute',
            top: '10%',
            left: '15%',
            right: '15%',
            bottom: '10%',
            border: '1px solid #ccc',
            overflow: 'auto',
            WebkitOverflowScrolling: 'touch',
            borderRadius: '25px',
            outline: 'none',
            padding: '0px'
          }
        }}
        contentLabel="Settings">
        <div className='bg-gradient-to-l from-teal-400 to-teal-100 w-full h-full p-2'>
          <button className={exitButtonStyle} onClick={() => _isSettingsOpen.set(false)}>
            <div className="scale-75 right">
              <img className="pl-2" src={closeIcon}/>
            </div>
          </button>
        </div>
      </Modal>
    </>
  )
}

export default SettingsModal
