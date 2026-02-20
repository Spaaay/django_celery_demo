import './ProfileCard.css'

function ProfileCard({ name, job, experience }) {
    return (
        <div>
            <h2>{name}</h2>
            <p>{job}</p>
            <p>{experience}</p>
        </div>
    )
}
export default ProfileCard