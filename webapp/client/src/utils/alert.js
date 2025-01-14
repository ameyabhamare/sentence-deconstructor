import React from 'react';
import { connect } from 'react-redux';

import { createAlert, closeAlert } from '../actions/alert';

const alertIcons = {
	'success': (
		<div class="flex items-center justify-center w-12 bg-green-500">
            <svg class="w-6 h-6 text-white fill-current" viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg">
                <path d="M20 3.33331C10.8 3.33331 3.33337 10.8 3.33337 20C3.33337 29.2 10.8 36.6666 20 36.6666C29.2 36.6666 36.6667 29.2 36.6667 20C36.6667 10.8 29.2 3.33331 20 3.33331ZM16.6667 28.3333L8.33337 20L10.6834 17.65L16.6667 23.6166L29.3167 10.9666L31.6667 13.3333L16.6667 28.3333Z"/>
            </svg>
        </div>
	),
	'error': (
		<div class="flex items-center justify-center w-12 bg-red-500">
            <svg class="w-6 h-6 text-white fill-current" viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg">
                <path d="M20 3.36667C10.8167 3.36667 3.3667 10.8167 3.3667 20C3.3667 29.1833 10.8167 36.6333 20 36.6333C29.1834 36.6333 36.6334 29.1833 36.6334 20C36.6334 10.8167 29.1834 3.36667 20 3.36667ZM19.1334 33.3333V22.9H13.3334L21.6667 6.66667V17.1H27.25L19.1334 33.3333Z"/>
            </svg>
        </div>
	),
	'info': (
		<div class="flex items-center justify-center w-12 bg-blue-500">
            <svg class="w-6 h-6 text-white fill-current" viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg">
                <path d="M20 3.33331C10.8 3.33331 3.33337 10.8 3.33337 20C3.33337 29.2 10.8 36.6666 20 36.6666C29.2 36.6666 36.6667 29.2 36.6667 20C36.6667 10.8 29.2 3.33331 20 3.33331ZM21.6667 28.3333H18.3334V25H21.6667V28.3333ZM21.6667 21.6666H18.3334V11.6666H21.6667V21.6666Z"/>
            </svg>
        </div>
	),
	'warning': (
		<div class="flex items-center justify-center w-12 bg-yellow-400">
             <svg class="w-6 h-6 text-white fill-current" viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg">
                <path d="M20 3.33331C10.8 3.33331 3.33337 10.8 3.33337 20C3.33337 29.2 10.8 36.6666 20 36.6666C29.2 36.6666 36.6667 29.2 36.6667 20C36.6667 10.8 29.2 3.33331 20 3.33331ZM21.6667 28.3333H18.3334V25H21.6667V28.3333ZM21.6667 21.6666H18.3334V11.6666H21.6667V21.6666Z"/>
            </svg>
        </div>
	)
};

const alertHeaders = {
	'success': (
		<span class="font-semibold text-green-500 dark:text-green-400">Success</span>
	),
	'error': (
		<span class="font-semibold text-red-500 dark:text-red-400">Error</span>
	),
	'info': (
		<span class="font-semibold text-blue-500 dark:text-blue-400">Info</span>
	),
	'warning': (
		<span class="font-semibold text-yellow-400 dark:text-yellow-300">Warning</span>
	)
}

const AlertBox = ({ message, type }) => (
	<div class="flex w-full max-w-sm mx-auto overflow-hidden bg-white rounded-lg shadow-md dark:bg-gray-800 mt-4">
        { alertIcons[type] }
        <div class="px-4 py-2 -mx-3 w-80">
            <div class="mx-3">
                { alertHeaders[type] }
                <p class="text-sm text-gray-600 dark:text-gray-200">{ message }</p>
            </div>
        </div>
    </div>
)

const Alert = (props) => {    

    return (
		<div className='absolute right-0 bottom-0 p-6 ph:p-3 z-50'>
			{props.alert.alerts.map(alert => (
				<AlertBox message={alert.message} type={alert.type} />
			))}
		</div>
    )    
}

export const showAlert = (message, type) => {
	const id = Math.floor(Math.random() * 1e9);
    createAlert(message, type, id);
	setTimeout(() => {
		closeAlert(id);
	}, 5000);
}

const mapStateToProps = (state) => ({
    alert: state.alert
})

export default connect(mapStateToProps)(Alert);