import type { ApiResponse } from "@/shared/types/api";

import { ApiRequestError, createApiRequestError } from "@/shared/api/errors";

/**
 * Достаёт полезные данные из нашего backend ApiResponse.
 *
 * Backend всегда возвращает обёртку:
 *
 * {
 *   data: ...,
 *   meta: {},
 *   errors: []
 * }
 *
 * Эта функция проверяет эту обёртку:
 * - если backend вернул errors, кидаем ApiRequestError;
 * - если data пустая, кидаем ApiRequestError;
 * - если всё хорошо, возвращаем только data.
 */
export function unwrapApiResponse<TData>(
  apiResponse: ApiResponse<TData>,
  status: number,
): TData {
  if (apiResponse.errors && apiResponse.errors.length > 0) {
    const firstError = apiResponse.errors[0];

    throw new ApiRequestError({
      status,
      message: firstError?.message ?? "Ошибка запроса",
      errors: apiResponse.errors,
      meta: apiResponse.meta,
      raw: apiResponse,
    });
  }

  if (apiResponse.data === undefined || apiResponse.data === null) {
    throw new ApiRequestError({
      status,
      message: "API вернул пустой ответ",
      raw: apiResponse,
    });
  }

  return apiResponse.data;
}

/**
 * Обрабатывает результат, который вернул openapi-fetch.
 *
 * apiClient.GET(...) возвращает объект:
 *
 * {
 *   data,
 *   error,
 *   response
 * }
 *
 * Эта функция проверяет внешний результат запроса:
 * - если есть error, значит HTTP-запрос завершился ошибкой 4xx/5xx;
 * - если data отсутствует, значит пришёл странный пустой ответ;
 * - если data есть, передаём её в unwrapApiResponse,
 *   чтобы достать полезные данные из нашей backend-обёртки.
 */
export function handleApiResult<TData>({
  apiResponse,
  error,
  response,
}: {
  apiResponse?: ApiResponse<TData>;
  error?: unknown;
  response: Response;
}): TData {
  if (error) {
    throw createApiRequestError({
      status: response.status,
      error,
    });
  }

  if (!apiResponse) {
    throw new ApiRequestError({
      status: response.status,
      message: "API вернул пустой ответ",
    });
  }

  return unwrapApiResponse(apiResponse, response.status);
}

/**
 * Обрабатывает API-запросы, у которых успешный ответ не содержит body.
 *
 * Например:
 * - logout
 * - delete
 * - endpoint с HTTP 204 No Content
 *
 * Если backend вернул ошибку, кидаем ApiRequestError.
 * Если ошибки нет, просто ничего не возвращаем.
 */
export function handleEmptyApiResult({
  error,
  response,
}: {
  error?: unknown;
  response: Response;
}): void {
  if (error) {
    throw createApiRequestError({
      status: response.status,
      error,
    });
  }

  if (!response.ok) {
    throw new ApiRequestError({
      status: response.status,
      message: "API-запрос завершился ошибкой",
    });
  }
}
