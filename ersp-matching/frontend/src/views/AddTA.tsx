import React, { useState, useEffect } from 'react';
import './FormStyles.css';

interface TAForm {
  name: string;
  email: string;
  professor_preferences: string[];
  class_level: boolean;
}

const AddTA: React.FC = () => {
  const [form, setForm] = useState<TAForm>({
    name: '',
    email: '',
    professor_preferences: [],
    class_level: false
  });
  const [allProfs, setAllProfs] = useState<any[]>([]);

  // Fetch all professors on mount
  useEffect(() => {
    fetch('http://localhost:8000/api/v1/professors/')
      .then(res => res.json())
      .then(data => setAllProfs(data));
  }, []);

  // Handle checkbox for professor preferences
  const handleCheckbox = (profName: string) => {
    setForm(prev => ({
      ...prev,
      professor_preferences: prev.professor_preferences.includes(profName)
        ? prev.professor_preferences.filter(n => n !== profName)
        : [...prev.professor_preferences, profName]
    }));
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value, type, checked } = e.target;
    setForm({ ...form, [name]: type === 'checkbox' ? checked : value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await fetch('http://localhost:8000/api/v1/teaching-assistants/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        ...form,
        professor_preferences: form.professor_preferences.join(',')
      })
    });
    alert('TA added!');
  };

  return (
    <form className="form-container" onSubmit={handleSubmit} style={{ color: "#222" }}>
      <div className="form-title">TA Registration</div>
      <div className="form-subtitle">TAs please fill out form carefully</div>
      <div className="form-row">
        <div>
          <label className="form-label" style={{ color: "#222" }}>TA Name</label>
          <input className="form-input" name="name" value={form.name} onChange={handleChange} required />
        </div>
        <div>
          <label className="form-label" style={{ color: "#222" }}>E-mail</label>
          <input className="form-input" name="email" value={form.email} onChange={handleChange} />
        </div>
      </div>
      <div className="form-row">
        <div>
          <label className="form-label" style={{ color: "#222" }}>PhD?</label>
          <input
            className="form-input"
            name="class_level"
            type="checkbox"
            checked={form.class_level}
            onChange={handleChange}
            style={{ width: 'auto', marginLeft: 8 }}
          />{' '}
          <span style={{ fontSize: '1rem', color: '#222' }}>{form.class_level ? 'Yes' : 'No'}</span>
        </div>
        <div>
          <label className="form-label" style={{ color: "#222" }}>Professor Preferences</label>
          <div style={{
            maxHeight: 150,
            minWidth: 250,
            overflowY: 'auto',
            border: '1px solid #ccc',
            borderRadius: 5,
            padding: 12,
            background: '#fafafa',
            color: "#222"
          }}>
            {allProfs.length === 0 && <div style={{ color: '#888', fontSize: '0.95em' }}>No professors available</div>}
            {allProfs.map(prof => (
              <div key={prof.id} style={{ marginBottom: 8 }}>
                <label style={{ color: "#222" }}>
                  <input
                    type="checkbox"
                    value={prof.name}
                    checked={form.professor_preferences.includes(prof.name)}
                    onChange={() => handleCheckbox(prof.name)}
                  />
                  <span style={{ marginLeft: 8, color: "#222" }}>{prof.name} {prof.email && `(${prof.email})`}</span>
                </label>
              </div>
            ))}
          </div>
        </div>
      </div>
      <button className="form-submit" type="submit">Submit</button>
    </form>
  );
};

export default AddTA;