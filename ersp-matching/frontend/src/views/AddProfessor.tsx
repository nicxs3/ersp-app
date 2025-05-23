import React, { useState, useEffect } from 'react';
import './FormStyles.css';

interface ProfessorForm {
  name: string;
  email: string;
  ta_preferences: string[];
  req_tas: number;
}

const AddProfessor: React.FC = () => {
  const [form, setForm] = useState<ProfessorForm>({
    name: '',
    email: '',
    ta_preferences: [],
    req_tas: 1
  });
  const [allTAs, setAllTAs] = useState<any[]>([]);
  const [filteredTAs, setFilteredTAs] = useState<any[]>([]);

  useEffect(() => {
    fetch('http://localhost:8000/api/v1/teaching-assistants/')
      .then(res => res.json())
      .then(data => setAllTAs(data));
  }, []);

  useEffect(() => {
    if (!form.name) {
      setFilteredTAs([]);
      return;
    }
    setFilteredTAs(
      allTAs.filter(ta =>
        ta.professor_preferences &&
        ta.professor_preferences.split(',').map((p: string) => p.trim()).includes(form.name)
      )
    );
  }, [form.name, allTAs]);

  const handleCheckbox = (taName: string) => {
    setForm(prev => ({
      ...prev,
      ta_preferences: prev.ta_preferences.includes(taName)
        ? prev.ta_preferences.filter(n => n !== taName)
        : [...prev.ta_preferences, taName]
    }));
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value, type } = e.target;
    setForm({ ...form, [name]: type === 'number' ? Number(value) : value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await fetch('http://localhost:8000/api/v1/professors/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        ...form,
        ta_preferences: form.ta_preferences.join(',')
      })
    });
    alert('Professor added!');
  };

  return (
    <form className="form-container" onSubmit={handleSubmit} style={{ color: "#222" }}>
      <div className="form-title">Professor Registration</div>
      <div className="form-subtitle">Professors please fill out form carefully</div>
      <div className="form-row">
        <div>
          <label className="form-label" style={{ color: "#222" }}>Professor Name</label>
          <input className="form-input" name="name" value={form.name} onChange={handleChange} required />
        </div>
        <div>
          <label className="form-label" style={{ color: "#222" }}>E-mail</label>
          <input className="form-input" name="email" value={form.email} onChange={handleChange} />
        </div>
      </div>
      <div className="form-row">
        <div>
          <label className="form-label" style={{ color: "#222" }}>Required TAs</label>
          <input className="form-input" name="req_tas" type="number" min="1" value={form.req_tas} onChange={handleChange} />
        </div>
        <div>
          <label className="form-label" style={{ color: "#222" }}>TA Preferences</label>
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
            {filteredTAs.length === 0 && <div style={{ color: '#888', fontSize: '0.95em' }}>Type professor name to see TAs</div>}
            {filteredTAs.map(ta => (
              <div key={ta.id} style={{ marginBottom: 8 }}>
                <label style={{ color: "#222" }}>
                  <input
                    type="checkbox"
                    value={ta.name}
                    checked={form.ta_preferences.includes(ta.name)}
                    onChange={() => handleCheckbox(ta.name)}
                  />
                  <span style={{ marginLeft: 8, color: "#222" }}>{ta.name} {ta.email && `(${ta.email})`}</span>
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

export default AddProfessor;