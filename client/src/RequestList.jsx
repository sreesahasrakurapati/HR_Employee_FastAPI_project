import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from './api';

function RequestList() {
    const navigate = useNavigate();

    const [requests, setRequests] = useState([]);

    const getRequests = async () => {
        const response = await api.get('/requests', {
            headers: {
                Authorization: `Bearer ${localStorage.getItem('token')}`
            }
        });

        setRequests(response.data);
    };

    const deleteRequest = async (id) => {
        await api.delete(`/requests/${id}`, {
            headers: {
                Authorization: `Bearer ${localStorage.getItem('token')}`
            }
        });

        getRequests();
    };

    useEffect(() => {
        getRequests();
    }, []);

    return (
        <div className="container mt-4">
            <div className="d-flex justify-content-between mb-3">
                <h2>Service Requests</h2>
                <button
                    className="btn btn-primary"
                    onClick={() => navigate('/requests/new')}
                >New Request</button>
            </div>
            <table className="table table-bordered table-striped">
                <thead>
                    <tr>
                        <th>Title</th>
                        <th>Description</th>
                        <th>Category</th>
                        <th>Status</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {requests.map(request => (
                        <tr key={request.id}>
                            <td>{request.title}</td>
                            <td>{request.description}</td>
                            <td>{request.category}</td>
                            <td>{request.status}</td>
                            <td>
                                <button
                                    className="btn btn-warning btn-sm me-2"
                                    onClick={() =>
                                        navigate(`/requests/edit/${request.id}`)
                                    }
                                >Edit</button>
                                <button
                                    className="btn btn-danger btn-sm"
                                    onClick={() =>
                                        deleteRequest(request.id)
                                    }
                                >Delete</button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

export default RequestList;
