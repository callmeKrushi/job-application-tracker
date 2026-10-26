import { useCallback, useEffect, useState } from 'react'
import './App.css'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'
const STATUSES = ['Applied', 'Interview', 'Selected', 'Rejected', 'Withdrawn']
const EMPTY_FORM = {
  company: '',
  role: '',
  location: '',
  job_type: 'Full-time',
  salary: '',
  job_url: '',
  notes: '',
  status: 'Applied',
  date_applied: new Date().toISOString().slice(0, 10),
  follow_up_date: '',
}

const navItems = [
  { label: 'Overview', icon: '◫' },
  { label: 'Applications', icon: '▤' },
]

function formatDate(value) {
  if (!value) return '—'
  const date = new Date(`${value}T00:00:00`)
  return Number.isNaN(date.getTime())
    ? value
    : new Intl.DateTimeFormat('en-IN', { day: 'numeric', month: 'short', year: 'numeric' }).format(date)
}

function statusClass(status) {
  return `status-pill status-${String(status || 'unknown').toLowerCase()}`
}

function followUpState(value) {
  if (!value) return { label: 'Not set', className: 'follow-up-none' }
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  const due = new Date(`${value}T00:00:00`)
  if (Number.isNaN(due.getTime())) return { label: 'Invalid date', className: 'follow-up-none' }
  const days = Math.round((due.getTime() - today.getTime()) / 86400000)
  if (days < 0) return { label: 'Overdue', className: 'follow-up-overdue' }
  if (days === 0) return { label: 'Due today', className: 'follow-up-today' }
  if (days <= 3) return { label: 'Due soon', className: 'follow-up-soon' }
  return { label: 'Scheduled', className: 'follow-up-scheduled' }
}

function App() {
  const [stats, setStats] = useState(null)
  const [responseRate, setResponseRate] = useState(null)
  const [monthly, setMonthly] = useState([])
  const [apiError, setApiError] = useState(false)
  const [activeNav, setActiveNav] = useState('Overview')

  const [applications, setApplications] = useState([])
  const [applicationCount, setApplicationCount] = useState(0)
  const [applicationsLoading, setApplicationsLoading] = useState(false)
  const [applicationsError, setApplicationsError] = useState('')
  const [search, setSearch] = useState('')
  const [statusFilter, setStatusFilter] = useState('All statuses')
  const [sortOrder, setSortOrder] = useState('desc')
  const [showForm, setShowForm] = useState(false)
  const [editingApplication, setEditingApplication] = useState(null)
  const [form, setForm] = useState(EMPTY_FORM)
  const [saving, setSaving] = useState(false)
  const [formError, setFormError] = useState('')
  const [notice, setNotice] = useState('')

  const loadDashboard = useCallback(async () => {
    try {
      const [statsResponse, rateResponse, monthlyResponse] = await Promise.all([
        fetch(`${API_BASE_URL}/stats`),
        fetch(`${API_BASE_URL}/stats/response-rate`),
        fetch(`${API_BASE_URL}/stats/monthly`),
      ])
      if (!statsResponse.ok || !rateResponse.ok || !monthlyResponse.ok) {
        throw new Error('Unable to load dashboard statistics')
      }
      const [statsData, rateData, monthlyData] = await Promise.all([
        statsResponse.json(),
        rateResponse.json(),
        monthlyResponse.json(),
      ])
      setStats(statsData)
      setResponseRate(rateData)
      setMonthly(monthlyData)
      setApiError(false)
    } catch {
      setApiError(true)
    }
  }, [])

  const loadApplications = useCallback(async () => {
    setApplicationsLoading(true)
    setApplicationsError('')
    try {
      const params = new URLSearchParams()
      params.set('sort', sortOrder)
      if (search.trim()) params.set('search', search.trim())
      if (statusFilter !== 'All statuses') params.set('status', statusFilter)
      const query = params.toString()
      const response = await fetch(`${API_BASE_URL}/applications${query ? `?${query}` : ''}`)
      if (!response.ok) throw new Error('Could not load applications.')
      const data = await response.json()
      setApplications(Array.isArray(data.applications) ? data.applications : [])
      setApplicationCount(Number(data.count ?? data.applications?.length ?? 0))
    } catch {
      setApplicationsError('We couldn’t load your applications. Check that the API is running, then try again.')
    } finally {
      setApplicationsLoading(false)
    }
  }, [search, statusFilter, sortOrder])

  useEffect(() => {
    loadDashboard()
  }, [loadDashboard])

  useEffect(() => {
    if (activeNav !== 'Applications') return undefined
    const timer = setTimeout(loadApplications, 250)
    return () => clearTimeout(timer)
  }, [activeNav, loadApplications])

  function openAddForm() {
    setEditingApplication(null)
    setForm(EMPTY_FORM)
    setFormError('')
    setShowForm(true)
  }

  function openEditForm(application) {
    setEditingApplication(application)
    setForm({
      company: application.company || '',
      role: application.role || '',
      location: application.location || '',
      job_type: application.job_type || 'Full-time',
      salary: application.salary || '',
      job_url: application.job_url || '',
      notes: application.notes || '',
      status: application.status || 'Applied',
      date_applied: application.date_applied || '',
      follow_up_date: application.follow_up_date || '',
    })
    setFormError('')
    setShowForm(true)
  }

  async function handleSubmitApplication(event) {
    event.preventDefault()
    setFormError('')
    setSaving(true)
    try {
      const payload = {
        company: form.company.trim(),
        role: form.role.trim(),
        location: form.location.trim() || null,
        job_type: form.job_type || null,
        salary: form.salary.trim() || null,
        job_url: form.job_url.trim() || null,
        notes: form.notes.trim() || null,
        status: form.status,
        follow_up_date: form.follow_up_date || null,
      }
      const isEditing = Boolean(editingApplication)
      if (!isEditing) payload.date_applied = form.date_applied
      const endpoint = isEditing
        ? `${API_BASE_URL}/applications/${editingApplication.id}`
        : `${API_BASE_URL}/applications`
      const response = await fetch(endpoint, {
        method: isEditing ? 'PATCH' : 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      })
      if (!response.ok) {
        const detail = await response.json().catch(() => null)
        throw new Error(detail?.detail || `Could not ${isEditing ? 'update' : 'save'} this application. Check the fields and try again.`)
      }
      setShowForm(false)
      setEditingApplication(null)
      setForm(EMPTY_FORM)
      setNotice(isEditing ? 'Application updated successfully.' : 'Application added successfully.')
      setActiveNav('Applications')
      await Promise.all([loadDashboard(), loadApplications()])
    } catch (error) {
      setFormError(error.message || 'Something went wrong. Please try again.')
    } finally {
      setSaving(false)
    }
  }

  async function handleStatusChange(application, nextStatus) {
    try {
      const response = await fetch(`${API_BASE_URL}/applications/${application.id}/status`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status: nextStatus }),
      })
      if (!response.ok) throw new Error('Status update failed')
      setNotice(`Status updated to ${nextStatus}.`)
      await Promise.all([loadApplications(), loadDashboard()])
    } catch {
      setApplicationsError('Could not update the status. Please try again.')
    }
  }

  async function handleDelete(application) {
    const confirmed = window.confirm(`Delete the application for ${application.company} — ${application.role}?`)
    if (!confirmed) return
    try {
      const response = await fetch(`${API_BASE_URL}/applications/${application.id}`, { method: 'DELETE' })
      if (!response.ok && response.status !== 204) throw new Error('Delete failed')
      setNotice('Application deleted.')
      await Promise.all([loadApplications(), loadDashboard()])
    } catch {
      setApplicationsError('Could not delete this application. Please try again.')
    }
  }

  useEffect(() => {
    if (!notice) return undefined
    const timer = setTimeout(() => setNotice(''), 3500)
    return () => clearTimeout(timer)
  }, [notice])

  const cards = [
    { label: 'Total applications', value: stats?.total, icon: '↗', tone: 'violet' },
    { label: 'Interviews', value: stats?.interview, icon: '✳', tone: 'blue' },
    { label: 'Offers & selections', value: stats?.selected, icon: '✦', tone: 'green' },
    { label: 'Response rate', value: responseRate ? `${responseRate.response_rate}%` : null, icon: '◎', tone: 'orange' },
  ]
  const maxMonthly = Math.max(1, ...monthly.map((item) => item.total))

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <a className="brand" href="#" onClick={(event) => { event.preventDefault(); setActiveNav('Overview') }}>
          <span className="brand-mark">c.</span>
          <span>career<span className="brand-light">flow</span></span>
        </a>

        <div className="workspace-label">WORKSPACE</div>
        <nav className="main-nav" aria-label="Main navigation">
          {navItems.map((item) => (
            <button
              className={`nav-item ${activeNav === item.label ? 'active' : ''}`}
              key={item.label}
              onClick={() => setActiveNav(item.label)}
            >
              <span className="nav-icon">{item.icon}</span>
              {item.label}
              {item.label === 'Applications' && stats && <span className="nav-count">{stats.total}</span>}
            </button>
          ))}
        </nav>

        <div className="sidebar-bottom">
          <div className="sidebar-tip">
            <span className="tip-icon">✦</span>
            <strong>Small steps count.</strong>
            <p>Your next opportunity starts with showing up.</p>
          </div>
          <div className="profile">
            <div className="avatar">KK</div>
            <div className="profile-info"><strong>My workspace</strong><span>Job seeker</span></div>
            <span className="profile-menu">···</span>
          </div>
        </div>
      </aside>

      <main className="main-content">
        <header className="topbar">
          <div className="breadcrumb">Workspace <span>/</span> {activeNav}</div>
          <div className="topbar-right">
            <span className={`live-dot ${apiError ? 'offline' : ''}`} />
            <span className="connection-label">
              {apiError ? 'API disconnected' : stats ? 'Connected to your tracker' : 'Connecting…'}
            </span>
            <div className="avatar small">KK</div>
          </div>
        </header>

        <div className="page-content">
          <section className="welcome-row">
            <div>
              <div className="eyebrow"><span /> YOUR CAREER, IN MOTION</div>
              <h1>{activeNav === 'Overview' ? 'Your next chapter.' : 'Your applications.'}</h1>
              <p className="page-subtitle">
                {activeNav === 'Overview'
                  ? 'One clear view of where you are and where you’re going.'
                  : 'Every opportunity, organized in one place.'}
              </p>
            </div>
            <button className="primary-button" onClick={openAddForm}>
              <span>＋</span> Add application
            </button>
          </section>

          {apiError && (
            <div className="api-notice" role="status">
              <span>ⓘ</span>
              <div><strong>We couldn’t reach your API.</strong><p>Start FastAPI on port 8000 to load your live tracker data.</p></div>
            </div>
          )}

          {notice && <div className="success-notice" role="status"><span>✓</span>{notice}<button onClick={() => setNotice('')} aria-label="Dismiss notification">×</button></div>}

          {activeNav === 'Overview' ? (
            <>
              <section className="stats-grid" aria-label="Application statistics">
                {cards.map((card) => (
                  <article className="stat-card" key={card.label}>
                    <div className="stat-card-top">
                      <span className="stat-label">{card.label}</span>
                      <span className={`stat-icon ${card.tone}`}>{card.icon}</span>
                    </div>
                    <div className="stat-value">{card.value ?? <span className="loading-value">—</span>}</div>
                    <div className="stat-foot">
                      <span className={`status-dot ${card.tone}`} />
                      {card.value == null ? 'Waiting for data' : 'From your application records'}
                    </div>
                  </article>
                ))}
              </section>

              <section className="content-grid">
                <article className="panel activity-panel">
                  <div className="panel-heading">
                    <div><h2>Application activity</h2><p>Your momentum, month by month.</p></div>
                    <span className="panel-badge">Monthly</span>
                  </div>
                  {monthly.length ? (
                    <div className="chart">
                      {monthly.slice(-6).map((item) => (
                        <div className="chart-column" key={item.month}>
                          <span className="bar-value">{item.total}</span>
                          <div className="bar-track"><div className="bar" style={{ height: `${Math.max(5, (item.total / maxMonthly) * 100)}%` }} /></div>
                          <span className="bar-label">{item.month}</span>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <div className="empty-chart">
                      <span className="empty-chart-icon">↗</span>
                      <strong>Your progress will show up here</strong>
                      <p>Add applications to start building your monthly activity chart.</p>
                    </div>
                  )}
                </article>

                <article className="panel pipeline-panel">
                  <div className="panel-heading">
                    <div><h2>Your pipeline</h2><p>Where things stand today.</p></div>
                    <span className="pipeline-symbol">◉</span>
                  </div>
                  <div className="pipeline-list">
                    {[
                      { label: 'Applied', key: 'applied', color: 'pipeline-violet' },
                      { label: 'Interview', key: 'interview', color: 'pipeline-blue' },
                      { label: 'Selected', key: 'selected', color: 'pipeline-green' },
                      { label: 'Rejected', key: 'rejected', color: 'pipeline-orange' },
                      { label: 'Withdrawn', key: 'withdrawn', color: 'pipeline-gray' },
                    ].map((item) => {
                      const count = stats?.[item.key] ?? 0
                      const total = stats?.total ?? 0
                      return (
                        <div className="pipeline-item" key={item.key}>
                          <div className="pipeline-label-row"><span><i className={item.color} />{item.label}</span><strong>{stats ? count : '—'}</strong></div>
                          <div className="pipeline-track"><div className={`pipeline-fill ${item.color}`} style={{ width: `${total ? (count / total) * 100 : 0}%` }} /></div>
                        </div>
                      )
                    })}
                  </div>
                  <div className="pipeline-footer"><span>Keep moving forward</span><span>✦</span></div>
                </article>
              </section>
            </>
          ) : (
            <section className="applications-panel panel">
              <div className="applications-toolbar">
                <div><h2>All applications <span className="results-count">{applicationCount}</span></h2><p>Keep track of every opportunity, from applied to offer.</p></div>
                <button className="secondary-button" onClick={loadApplications}>↻ Refresh</button>
              </div>
              <div className="follow-up-summary">
                {[
                  { label: 'Overdue', count: applications.filter((item) => item.follow_up_date && followUpState(item.follow_up_date).className === 'follow-up-overdue').length, tone: 'overdue' },
                  { label: 'Due today', count: applications.filter((item) => item.follow_up_date && followUpState(item.follow_up_date).className === 'follow-up-today').length, tone: 'today' },
                  { label: 'Due soon', count: applications.filter((item) => item.follow_up_date && followUpState(item.follow_up_date).className === 'follow-up-soon').length, tone: 'soon' },
                ].map((item) => (
                  <div className={`follow-up-stat ${item.tone}`} key={item.label}>
                    <span>{item.label}</span><strong>{item.count}</strong>
                  </div>
                ))}
              </div>
              <div className="application-filters">
                <label className="search-box"><span>⌕</span><input value={search} onChange={(event) => setSearch(event.target.value)} placeholder="Search company or role…" aria-label="Search company or role" /><kbd>/</kbd></label>
                <select value={statusFilter} onChange={(event) => setStatusFilter(event.target.value)} aria-label="Filter by status">
                  <option>All statuses</option>
                  {STATUSES.map((status) => (<option key={status}>{status}</option>))}
                </select>
                  {/* NEW: Sorting dropdown */}
                  <select
                    value={sortOrder}
                    onChange={(event) => setSortOrder(event.target.value)}
                    aria-label="Sort applications by date"
                  >
                    <option value="desc">Newest first</option>
                    <option value="asc">Oldest first</option>
                  </select>
              </div>

              {applicationsError && <div className="inline-error" role="alert">{applicationsError}<button onClick={loadApplications}>Try again</button></div>}
              {applicationsLoading ? (
                <div className="applications-empty"><span className="loading-spinner" /><strong>Loading applications…</strong></div>
              ) : applications.length ? (
                <div className="applications-table-wrap">
                  <table className="applications-table">
                    <thead><tr><th>COMPANY & ROLE</th><th>LOCATION</th><th>DATE APPLIED</th><th>FOLLOW-UP</th><th>STATUS</th><th><span className="sr-only">Actions</span></th></tr></thead>
                    <tbody>
                      {applications.map((application) => (
                        <tr key={application.id}>
                          <td>
                            <div className="company-cell">
                              <span className="company-logo">{String(application.company || '?').trim().charAt(0).toUpperCase()}</span>
                              <span><strong>{application.company || 'Unnamed company'}</strong><small>{application.role || 'Role not specified'}</small></span>
                            </div>
                          </td>
                          <td>{application.location || <span className="muted-value">Not specified</span>}</td>
                          <td>{formatDate(application.date_applied)}</td>
                          <td>
                            {application.follow_up_date ? (
                              <div className="follow-up-cell">
                                <span>{formatDate(application.follow_up_date)}</span>
                                <small className={followUpState(application.follow_up_date).className}>{followUpState(application.follow_up_date).label}</small>
                              </div>
                            ) : <span className="muted-value">Not set</span>}
                          </td>
                          <td>
                            <select className={statusClass(application.status)} value={application.status || 'Applied'} onChange={(event) => handleStatusChange(application, event.target.value)} aria-label={`Status for ${application.company} ${application.role}`}>
                              {STATUSES.map((status) => <option key={status}>{status}</option>)}
                            </select>
                          </td>
                          <td className="row-actions">
                            {application.job_url && <a href={application.job_url} target="_blank" rel="noreferrer" title="Open job posting" aria-label="Open job posting">↗</a>}
                            <button onClick={() => openEditForm(application)} title="Edit application" aria-label={`Edit ${application.company} application`}>✎</button>
                            <button onClick={() => handleDelete(application)} title="Delete application" aria-label={`Delete ${application.company} application`}>×</button>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              ) : (
                <div className="applications-empty">
                  <span className="empty-app-icon">▤</span>
                  <h3>{search || statusFilter !== 'All statuses' ? 'No matching applications' : 'Your next opportunity starts here'}</h3>
                  <p>{search || statusFilter !== 'All statuses' ? 'Try a different search or status filter.' : 'Add your first application and keep your job search organized.'}</p>
                  {search || statusFilter !== 'All statuses'
                    ? <button className="secondary-button" onClick={() => { setSearch(''); setStatusFilter('All statuses') }}>Clear filters</button>
                    : <button className="primary-button" onClick={openAddForm}>＋ Add application</button>}
                </div>
              )}
              <div className="table-footer"><span>Showing {applications.length} of {applicationCount} matching applications</span><span>Changes save to your tracker</span></div>
            </section>
          )}

          <footer className="page-footer"><span>Made for the next chapter.</span><span>Careerflow <i /> Personal job tracker</span></footer>
        </div>
      </main>

      {showForm && (
        <div className="modal-backdrop" onMouseDown={(event) => { if (event.target === event.currentTarget) setShowForm(false) }}>
          <section className="application-modal" role="dialog" aria-modal="true" aria-labelledby="form-title">
            <div className="modal-heading">
              <div><span className="modal-eyebrow">{editingApplication ? 'UPDATE OPPORTUNITY' : 'NEW OPPORTUNITY'}</span><h2 id="form-title">{editingApplication ? 'Edit application' : 'Add an application'}</h2><p>{editingApplication ? 'Update the details for this opportunity.' : 'Capture the details now. You can keep the rest simple.'}</p></div>
              <button className="modal-close" onClick={() => { setShowForm(false); setEditingApplication(null) }} aria-label="Close form">×</button>
            </div>
            <form onSubmit={handleSubmitApplication}>
              <div className="form-grid">
                <label>Company <span>*</span><input required maxLength={150} value={form.company} onChange={(event) => setForm({ ...form, company: event.target.value })} placeholder="e.g. Google" /></label>
                <label>Job title <span>*</span><input required maxLength={150} value={form.role} onChange={(event) => setForm({ ...form, role: event.target.value })} placeholder="e.g. Python Developer" /></label>
                <label>Location<input value={form.location} onChange={(event) => setForm({ ...form, location: event.target.value })} placeholder="e.g. Hyderabad / Remote" /></label>
                <label>Employment type<select value={form.job_type} onChange={(event) => setForm({ ...form, job_type: event.target.value })}><option>Full-time</option><option>Part-time</option><option>Internship</option><option>Contract</option><option>Remote</option><option>Other</option></select></label>
                <label>Salary / CTC<input value={form.salary} onChange={(event) => setForm({ ...form, salary: event.target.value })} placeholder="e.g. 8 LPA or ₹40,000/month" /></label>
                <label>Date applied<input type="date" required value={form.date_applied} disabled={Boolean(editingApplication)} onChange={(event) => setForm({ ...form, date_applied: event.target.value })} />{editingApplication && <small className="field-hint">The application date is preserved when editing.</small>}</label>
                <label className="form-full">Job posting URL<input type="url" value={form.job_url} onChange={(event) => setForm({ ...form, job_url: event.target.value })} placeholder="https://…" /></label>
                <label>Status<select value={form.status} onChange={(event) => setForm({ ...form, status: event.target.value })}>{STATUSES.map((status) => <option key={status}>{status}</option>)}</select></label>
                <label>Follow-up date<input type="date" min={new Date().toISOString().slice(0, 10)} value={form.follow_up_date} onChange={(event) => setForm({ ...form, follow_up_date: event.target.value })} /><small className="field-hint">Optional. Choose when you want to check in.</small></label>
                <label className="form-full">Notes<textarea rows="3" value={form.notes} onChange={(event) => setForm({ ...form, notes: event.target.value })} placeholder="Referral details, contact person, next steps…" /></label>
              </div>
              {formError && <div className="inline-error" role="alert">{formError}</div>}
              <div className="modal-actions"><button type="button" className="secondary-button" onClick={() => { setShowForm(false); setEditingApplication(null) }} disabled={saving}>Cancel</button><button type="submit" className="primary-button" disabled={saving}>{saving ? (editingApplication ? 'Updating…' : 'Saving…') : (editingApplication ? 'Save changes' : 'Save application')}</button></div>
            </form>
          </section>
        </div>
      )}
    </div>
  )
}

export default App
