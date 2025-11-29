import Link from 'next/link';
import {User} from "@/types/users";




const Users = async () => {
    const res = await fetch('https://jsonplaceholder.typicode.com/users');
    const users: User[] = await res.json();
    return (
        <div>
            <h1>Список пользователей </h1>
            <ul>
                {users.map(user => (
                    <li key={user.id}>
                        <Link href={`/users/${user.id}`} className="text-blue-500 hover:underline">
                            {user.name}
                        </Link>
                    </li>
                ))}
            </ul>

        </div>
    );
};

export default Users;