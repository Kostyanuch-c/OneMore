import { User } from '@/types/users';
import Link from 'next/link';

interface Props {
  params: Promise<{ id: string }>
}

export default async function UserPage({ params }: Props) {
  const { id } = await params; // разворачиваем Promise
  const res = await fetch(`https://jsonplaceholder.typicode.com/users/${id}`);
  const user: User = await res.json();
  return (
    <div>
      <h1>Пользователь c id {user.id} и именем {user.name}</h1>
      <Link href="/users">Назад</Link>
    </div>
  );
}