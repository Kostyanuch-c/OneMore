import Cookies from "js-cookie";

export function getCsrfHeaders(): HeadersInit | undefined {
  const csrfToken = Cookies.get("csrftoken");

  if (!csrfToken) {
    return undefined;
  }

  return {
    "X-CSRFToken": csrfToken,
  };
}
