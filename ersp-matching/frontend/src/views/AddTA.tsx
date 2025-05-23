import React, { useState } from 'react';

const AddTA: React.FC = () => {
  const [form, setForm] = useState({
    name: '',
    email: '',
    professor_preferences: '',
    class_level: false // boolean: true for PhD, false for others
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value, type, checked } = e.target;
    setForm({ ...form, [name]: type === 'checkbox' ? checked : value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await fetch('http://localhost:8000/api/v1/teaching-assistants/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form)
    });
    alert('TA added!');
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Add TA</h2>
      <input name="name" placeholder="Name" value={form.name} onChange={handleChange} required />
      <input name="email" placeholder="Email" value={form.email} onChange={handleChange} />
      <input
        name="professor_preferences"
        placeholder="Professor Preferences (comma separated)"
        value={form.professor_preferences}
        onChange={handleChange}
        />
      <label>
        PhD?
        <input name="class_level" type="checkbox" checked={form.class_level} onChange={handleChange} />
      </label>
      <button type="submit">Add TA</button>
    </form>
  );
};

export default AddTA;