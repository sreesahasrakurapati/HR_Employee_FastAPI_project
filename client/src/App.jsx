import { BrowserRouter, Routes, Route, Link, Navigate, useNavigate } from 'react-router-dom';

import Login from './Login';
import Register from './Register';
import RequestList from './RequestList';
import RequestForm from './RequestForm';


function ProtectedRoute({ children }) {
    const token = localStorage.getItem('token');

    return token ? children : <Navigate to="/login" />;
}

function Navigation() {
    const navigate = useNavigate();
    const token = localStorage.getItem('token');
    const username = localStorage.getItem('username');
    const logout = () => {
        localStorage.removeItem('token');
        localStorage.removeItem('username');
        navigate('/login');
    };
    return (
       <nav className="navbar navbar-dark bg-dark px-3">

            <Link className="navbar-brand" to={token ? "/requests" : "/login"}>
                HR Service Request Portal
            </Link>

            <div>
                {token ? (
                    <>
                        <Link className="btn btn-light me-2" to="/requests">
                            Requests
                        </Link>

                        <Link className="btn btn-light me-2" to="/requests/new">
                            New Request
                        </Link>

                        <Link className="btn btn-light me-2" to="/register">
                            Register
                        </Link>

                        <span className="text-white me-3">
                            {username}
                        </span>

                        <button
                            className="btn btn-danger"
                            onClick={logout}
                        >
                            Logout
                        </button>
                    </>
                ) : (
                    <>
                        <Link className="btn btn-light me-2" to="/login">
                            Login
                        </Link>

                        <Link className="btn btn-light" to="/register">
                            Register
                        </Link>
                    </>
                )}
            </div>

        </nav>
    );
}

function App() {
    return (
        <BrowserRouter>

            <Navigation />

            <Routes>

                <Route
                    path="/"
                    element={
                        localStorage.getItem('token')
                            ? <Navigate to="/requests" />
                            : <Navigate to="/login" />
                    }
                />

                <Route path="/login" element={<Login />} />

                <Route
                    path="/requests"
                    element={
                        <ProtectedRoute>
                            <RequestList />
                        </ProtectedRoute>
                    }
                />

                <Route
                    path="/requests/new"
                    element={
                        <ProtectedRoute>
                            <RequestForm />
                        </ProtectedRoute>
                    }
                />

                <Route
                    path="/requests/edit/:id"
                    element={
                        <ProtectedRoute>
                            <RequestForm />
                        </ProtectedRoute>
                    }
                />

                <Route
                    path="/register"
                    element={
                        <Register />
                    }
                />

            </Routes>

        </BrowserRouter>
    );
}

export default App;
