import '../style/login.css'

export default function Voting(){
    return(
        <div className="main-container">
        <div className="login">
            <h1>Login</h1>
            <div className="login-container">
                <div className="option-container">
                    <p>Username</p>
                    <input id="username" placeholder="Enter username">
                    </input>
                </div>
                <div className="option-container">
                    <p>Password</p>
                    <input id="password" type="password" placeholder="Enter password"></input>
                </div>
                <button>Login</button>
            </div>
        </div>
    </div>
    );
}