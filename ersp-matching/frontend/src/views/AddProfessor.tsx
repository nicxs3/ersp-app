import React, { useState } from 'react';

const AddProfessor: React.FC = () => {
  const [form, setForm] = useState({
    name: '',
    email: '',
    ta_preferences: '',
    req_tas: 1
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await fetch('http://localhost:8000/api/v1/professors/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form)
    });
    alert('Professor added!');
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Add Professor</h2>
      <input name="name" placeholder="Name" value={form.name} onChange={handleChange} required />
      <input name="email" placeholder="Email" value={form.email} onChange={handleChange} />
      <input name="ta_preferences" placeholder="TA Preferences (comma separated)" value={form.ta_preferences} onChange={handleChange} />
      <input name="req_tas" type="number" min="1" value={form.req_tas} onChange={handleChange} />
      <button type="submit">Add Professor</button>
    </form>
  );
};

export default AddProfessor;