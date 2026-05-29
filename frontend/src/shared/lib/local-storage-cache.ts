interface CacheEntry<T> {
  data: T;
  expiresAt: number;
}

interface LocalStorageCacheOptions<T> {
  key: string;
  ttl: number;
  fetcher: () => Promise<T>;
}

function removeLocalStorageItem(key: string): void {
  try {
    localStorage.removeItem(key);
  } catch {
    // localStorage может быть недоступен
  }
}

export async function withLocalStorageCache<T>({
  key,
  ttl,
  fetcher,
}: LocalStorageCacheOptions<T>): Promise<T> {
  if (typeof window !== "undefined") {
    try {
      const cached = localStorage.getItem(key);

      if (cached) {
        const parsed = JSON.parse(cached) as CacheEntry<T>;

        if (Date.now() < parsed.expiresAt) {
          return parsed.data;
        }

        removeLocalStorageItem(key);
      }
    } catch {
      removeLocalStorageItem(key);
    }
  }

  const data = await fetcher();

  if (typeof window !== "undefined") {
    try {
      localStorage.setItem(
        key,
        JSON.stringify({
          data,
          expiresAt: Date.now() + ttl,
        }),
      );
    } catch {
      // localStorage может быть недоступен или переполнен
    }
  }

  return data;
}
