import type { ApiErrorItem, ApiResponse } from "@/shared/types/api";

import { isRecord } from "@/shared/lib/type-guards";

const DEFAULT_ERROR_MESSAGES: Record<number, string> = {
  400: "Некорректный запрос",
  401: "Необходима авторизация",
  403: "Недостаточно прав",
  404: "Не найдено",
  409: "Конфликт данных",
  422: "Ошибка валидации",
};

function getDefaultErrorMessage(status: number): string {
  if (status >= 500) {
    return "Ошибка сервера";
  }

  return DEFAULT_ERROR_MESSAGES[status] ?? "Ошибка запроса";
}

export class ApiRequestError extends Error {
  readonly status: number;
  readonly errors: ApiErrorItem[];
  readonly meta: Record<string, unknown>;
  readonly raw?: unknown;

  constructor(params: {
    status: number;
    message: string;
    errors?: ApiErrorItem[];
    meta?: Record<string, unknown>;
    raw?: unknown;
  }) {
    super(params.message);

    this.name = "ApiRequestError";
    this.status = params.status;
    this.errors = params.errors ?? [
      {
        message: params.message,
        extra: {},
      },
    ];
    this.meta = params.meta ?? {};
    this.raw = params.raw;
  }

  get firstError(): ApiErrorItem | undefined {
    return this.errors[0];
  }
  get messages(): string[] {
    return this.errors.map((error) => error.message);
  }
  get isNotFound(): boolean {
    return this.status === 404;
  }

  get isUnauthorized(): boolean {
    return this.status === 401;
  }

  get isForbidden(): boolean {
    return this.status === 403;
  }

  get isValidationError(): boolean {
    return this.status === 422;
  }

  get isServerError(): boolean {
    return this.status >= 500;
  }
}

function isApiResponse(value: unknown): value is ApiResponse {
  return isRecord(value) && Array.isArray(value.errors);
}

export function createApiRequestError(params: {
  status: number;
  error: unknown;
}): ApiRequestError {
  const { status, error } = params;

  if (isApiResponse(error)) {
    const firstError = error.errors?.[0];

    return new ApiRequestError({
      status,
      message: firstError?.message ?? getDefaultErrorMessage(status),
      errors: error.errors,
      meta: error.meta,
      raw: error,
    });
  }

  return new ApiRequestError({
    status,
    message: getDefaultErrorMessage(status),
    raw: error,
  });
}
