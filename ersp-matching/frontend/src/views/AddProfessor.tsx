import React, { useState, useEffect } from 'react';

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

  // Fetch all TAs on mount
  useEffect(() => {
    fetch('http://localhost:8000/api/v1/teaching-assistants/')
      .then(res => res.json())
      .then(data => setAllTAs(data));
  }, []);

  // Filter TAs as professor name changes
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

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value, type } = e.target;
    if (name === 'ta_preferences') {
      // For multi-select, value is an array of selected options
      const options = (e.target as HTMLSelectElement).selectedOptions;
      const values = Array.from(options).map(option => option.value);
      setForm({ ...form, [name]: values });
    } else {
      setForm({ ...form, [name]: type === 'number' ? Number(value) : value });
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await fetch('http://localhost:8000/api/v1/professors/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        ...form,
        ta_preferences: form.ta_preferences.join(',') // send as comma-separated string
      })
    });
    alert('Professor added!');
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Add Professor</h2>
      <input name="name" placeholder="Name" value={form.name} onChange={handleChange} required />
      <input name="email" placeholder="Email" value={form.email} onChange={handleChange} />
      <input name="req_tas" type="number" min="1" value={form.req_tas} onChange={handleChange} />
      <label>
        TA Preferences:
        <div style={{ maxHeight: 200, overflowY: 'auto', border: '1px solid #ccc', padding: 8 }}>
            {filteredTAs.map(ta => (
            <div key={ta.id}>
                <label>
                <input
                    type="checkbox"
                    value={ta.name}
                    checked={form.ta_preferences.includes(ta.name)}
                    onChange={e => {
                    if (e.target.checked) {
                        setForm({ ...form, ta_preferences: [...form.ta_preferences, ta.name] });
                    } else {
                        setForm({ ...form, ta_preferences: form.ta_preferences.filter(n => n !== ta.name) });
                    }
                    }}
                />
                {ta.name} ({ta.email})
                </label>
            </div>
            ))}
        </div>
    </label>
      <button type="submit">Add Professor</button>
    </form>
  );
};

export default AddProfessor;