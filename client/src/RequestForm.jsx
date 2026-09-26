import { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import api from './api';

function RequestForm() {

    const navigate = useNavigate();
    const { id } = useParams();

    const [form, setForm] = useState({
        title: '',
        description: '',
        category: '',
        status: 'NEW'
    });

    const token = localStorage.getItem('token');

    useEffect(() => {
        if (id) {
            getRequest();
        }
    }, [id]);

    const getRequest = async () => {
        const response = await api.get(`/requests/${id}`, {
            headers: {
                Authorization: `Bearer ${token}`
            }
        });

        setForm(response.data);
    };

    const saveRequest = async () => {

        if (id) {
            await api.put(`/requests/${id}`, form, {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            });

            alert('Request updated');
        } else {
            await api.post('/requests', form, {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            });

            alert('Request submitted');
        }

        navigate('/requests');
    };

    return (
        <div className="container mt-4">

            <div className="card p-4 mx-auto" style={{maxWidth: '600px'}}>

                <h2>
                    {id ? 'Edit Request' : 'New Request'}
                </h2>

                <label className="form-label">Title</label>

                <input
                    className="form-control mb-3"
                    value={form.title}
                    onChange={e =>
                        setForm({
                            ...form,
                            title: e.target.value
                        })
                    }
                />

                <label className="form-label">Description</label>

                <textarea
                    className="form-control mb-3"
                    value={form.description}
                    onChange={e =>
                        setForm({
                            ...form,
                            description: e.target.value
                        })
                    }
                />

                <label className="form-label">Category</label>

                <select
                    className="form-select mb-3"
                    value={form.category}
                    onChange={e =>
                        setForm({
                            ...form,
                            category: e.target.value
                        })
                    }
                >
                    <option value="">Select Category</option>
                    <option value="Payroll">Payroll</option>
                    <option value="Leave">Leave</option>
                    <option value="Onboarding">Onboarding</option>
                    <option value="IT Access">IT Access</option>
                    <option value="Benefits">Benefits</option>
                    <option value="Grievance">Grievance</option>
                </select>

                <label className="form-label">Status</label>

                <select
                    className="form-select mb-3"
                    value={form.status}
                    onChange={e =>
                        setForm({
                            ...form,
                            status: e.target.value
                        })
                    }
                >
                    <option value="NEW">NEW</option>
                    <option value="ASSIGNED">ASSIGNED</option>
                    <option value="IN_PROGRESS">IN_PROGRESS</option>
                    <option value="ON_HOLD">ON_HOLD</option>
                    <option value="RESOLVED">RESOLVED</option>
                    <option value="CLOSED">CLOSED</option>
                </select>

                <button
                    className="btn btn-primary"
                    onClick={saveRequest}
                >
                    {id ? 'Update Request' : 'Submit Request'}
                </button>

            </div>

        </div>
    );
}

export default RequestForm;
