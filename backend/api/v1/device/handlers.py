from django.http import HttpRequest

from ninja import (
    File,
    Form,
    Query,
    Router,
    UploadedFile,
)

from api.filters import (
    PaginationIn,
    PaginationOut,
)
from api.schemas import (
    ApiResponse,
    ListPaginationResponse,
)
from api.v1.device.shemas import (
    BrandOutShema,
    DeviceOutShema,
    TypeOutShema,
)
from apps.devices.entities import (
    BrandInputSchema,
    DeviceInputSchema,
    TypeInputSchema,
)
from apps.devices.services.device_service import (
    BrandService,
    DeviceService,
    TypeService,
)

router = Router(tags=['devices'])


@router.post('/brand', response=ApiResponse[BrandOutShema])
def create_brand(
    request: HttpRequest, payload: BrandInputSchema
) -> ApiResponse[BrandOutShema]:
    brand = BrandService().create_brand(payload.name)
    return ApiResponse.success(
        data=BrandOutShema.from_entity(brand),
    )


@router.get(
    '/brand', response=ApiResponse[ListPaginationResponse[BrandOutShema]]
)
def get_brand_list(
    request: HttpRequest, pagination_in: Query[PaginationIn]
) -> ApiResponse[ListPaginationResponse[BrandOutShema]]:
    items = [
        BrandOutShema.from_entity(obj)
        for obj in BrandService().get_list_brands()
    ]

    pagination_out = PaginationOut(
        limit=pagination_in.limit, offset=pagination_in.offset, total=20
    )
    return ApiResponse.success(
        data=ListPaginationResponse(items=items, pagination=pagination_out),
    )


@router.get(
    '/type', response=ApiResponse[ListPaginationResponse[TypeOutShema]]
)
def get_types_list(
    request: HttpRequest, pagination_in: Query[PaginationIn]
) -> ApiResponse[ListPaginationResponse[TypeOutShema]]:
    items = [
        TypeOutShema.from_entity(obj) for obj in TypeService().get_list_types()
    ]

    pagination_out = PaginationOut(
        limit=pagination_in.limit, offset=pagination_in.offset, total=20
    )
    return ApiResponse.success(
        data=ListPaginationResponse(items=items, pagination=pagination_out),
    )


@router.post('/type', response=ApiResponse[TypeOutShema])
def create_type(
    request: HttpRequest, payload: TypeInputSchema
) -> ApiResponse[TypeOutShema]:
    type = TypeService().create_type(payload.name)
    return ApiResponse.success(
        data=TypeOutShema.from_entity(type),
    )


@router.post('/device', response=ApiResponse[DeviceOutShema])
def create_device(
    request: HttpRequest,
    payload: Form[DeviceInputSchema],
    img: UploadedFile | None = File(None),  # type: ignore
) -> ApiResponse[DeviceOutShema]:
    device = DeviceService().create_device(
        name=payload.name,
        brand_id=payload.brand_id,
        type_id=payload.type_id,
        img_file=img,
        price=payload.price,
    )
    return ApiResponse.success(
        data=DeviceOutShema.from_entity(device),
    )


@router.get('/device', response=ApiResponse[ListPaginationResponse[DeviceOutShema]])
def get_devices_list(
    request: HttpRequest, pagination_in: Query[PaginationIn]) -> ApiResponse[ListPaginationResponse[DeviceOutShema]]:
    items = [DeviceOutShema.from_entity(obj) for obj in DeviceService().get_list_devices()]
    pagination_out = PaginationOut(
        limit=pagination_in.limit, offset=pagination_in.offset, total=20
    )
    return ApiResponse.success(
        data=ListPaginationResponse(items=items, pagination=pagination_out),
    )
