from dataclasses import dataclass, field
from pathlib import Path
from typing import (
    Any,
    Hashable,
    Iterable,
    List,
    Optional,
    Tuple,
    Dict,
    Union,
    Sequence,
    Type,
    cast,
)


from .pyside import QtCore
from .listener import ClassWithListener
from ..core import gpg
from ..core.metadata import Purpose
from ..core.secret import Secret
from ..utils.config import Config
from ..protocols import Protocol, sftp, liquid_files, s3
from .listener import ListenerWrap

INDEX_UNION_TYPE = Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]

# Default value Qt.DisplayRole for index is not an int (upstream issue).
default_display_role = cast(int, QtCore.Qt.DisplayRole)


class TableModel(QtCore.QAbstractTableModel):
    def __init__(
        self,
        data: Sequence[Sequence[Any]] = (),
        columns: Optional[Tuple[str, ...]] = None,
    ):
        super().__init__()
        self.set_data(data or tuple(tuple()))
        self.columns = columns or tuple(map(str, range(self.columnCount())))

    @property
    def columns(self) -> Tuple[str, ...]:
        return self._columns

    @columns.setter
    def columns(self, values: Sequence[str]) -> None:
        self._columns = tuple(values)

    def get_data(self) -> Tuple[Sequence[Any], ...]:
        return self._data

    def set_data(self, data: Sequence[Sequence[Any]]) -> None:
        self._data = tuple(sorted(tuple(x) for x in data))
        self.layoutChanged.emit()  # type: ignore
        self.dataChanged.emit(  # type: ignore
            self.createIndex(0, 0),
            self.createIndex(self.rowCount(), self.columnCount()),
        )

    def rowCount(self, _parent: INDEX_UNION_TYPE = QtCore.QModelIndex()) -> int:
        return len(self._data)

    def columnCount(self, _parent: INDEX_UNION_TYPE = QtCore.QModelIndex()) -> int:
        return len(self._data) and len(self._data[0])

    def headerData(
        self,
        section: int,
        orientation: QtCore.Qt.Orientation = QtCore.Qt.Horizontal,
        role: int = default_display_role,
    ) -> Optional[str]:
        if orientation == QtCore.Qt.Horizontal and role == default_display_role:
            return self._columns[section]
        if orientation == QtCore.Qt.Vertical and role == default_display_role:
            return str(section)
        return None

    def data(
        self, index: INDEX_UNION_TYPE, role: int = default_display_role
    ) -> Optional[Any]:
        if role == default_display_role:
            return self._data[index.row()][index.column()]
        return None

    def removeRows(
        self, row: int, count: int, _parent: INDEX_UNION_TYPE = QtCore.QModelIndex()
    ) -> bool:
        if row > -1 and row + count <= self.rowCount():
            self.beginRemoveRows(QtCore.QModelIndex(), row, row + count - 1)
            self.set_data(self.get_data()[:row] + self.get_data()[row + count :])
            self.endRemoveRows()
            return True
        return False


class KeyValueListModel(QtCore.QAbstractListModel):
    """List model extension for key-value objects."""

    def __init__(
        self,
        *args: Any,
        data: Optional[Iterable[Tuple[Hashable, Any]]] = None,
        **kwargs: Any,
    ):
        super().__init__(*args, **kwargs)
        self.set_data(data or [])

    def set_data(self, data: Iterable[Tuple[Hashable, Any]]) -> None:
        self._keyvalues = dict(data)
        self._keys = list(self._keyvalues.keys())
        self.layoutChanged.emit()  # type: ignore

    # Default value Qt.DisplayRole for index is not an int (upstream issue):
    def data(self, index, role) -> Optional[Hashable]:  # type: ignore
        if role == QtCore.Qt.DisplayRole:
            key: Hashable = self._keys[index.row()]
            return key
        return None

    def rowCount(self, _parent: INDEX_UNION_TYPE = QtCore.QModelIndex()) -> int:
        return len(self._keys)

    def get_value(self, index: Union[int, QtCore.QModelIndex]) -> Any:
        if isinstance(index, int):
            return self._keyvalues[self._keys[index]]
        if isinstance(index, QtCore.QModelIndex):
            return self._keyvalues[self._keys[index.row()]]
        raise TypeError("Wrong index type for index.")


def protocol_factory() -> Dict[Type[Protocol], ListenerWrap]:
    return {
        sftp.Protocol: ListenerWrap(new_sftp_connection()),
        s3.Protocol: ListenerWrap(new_s3_connection()),
        liquid_files.Protocol: ListenerWrap(new_liquid_files_connection()),
    }


def new_sftp_connection() -> Protocol:
    return sftp.Protocol(host="", username="", destination_dir="")


def new_s3_connection() -> Protocol:
    return s3.Protocol(host="", bucket="", access_key="", secret_key=Secret(""))


def new_liquid_files_connection() -> Protocol:
    return liquid_files.Protocol(host="", api_key=Secret(""))


@dataclass
class AppData(ClassWithListener):
    """Settings that are specific to the sett GUI."""

    config: Config

    encrypt_sender: Optional[str] = None
    encrypt_recipients: Tuple[str, ...] = ()
    encrypt_transfer_id: Optional[int] = None
    encrypt_purpose: Optional[Purpose] = None
    encrypt_compression_level: int = 6
    encrypt_output_location: Path = field(default_factory=Path.home)
    encrypt_files: List[str] = field(default_factory=list)
    encrypt_verify_dtr: bool = True
    encrypt_package_name_suffix: str = ""
    encrypt_ignore_disk_space_error: bool = False

    decrypt_decrypt_only: bool = False
    decrypt_output_location: Path = field(default_factory=Path.home)
    decrypt_files: List[str] = field(default_factory=list)

    transfer_protocol_type: Type[Protocol] = sftp.Protocol
    transfer_protocol_args: Dict[Type[Protocol], ListenerWrap] = field(
        default_factory=protocol_factory
    )
    transfer_files: List[str] = field(default_factory=list)
    transfer_verify_dtr: bool = True
    transfer_verify_package_name: bool = True

    priv_keys_model: KeyValueListModel = field(default_factory=KeyValueListModel)
    pub_keys_model: KeyValueListModel = field(default_factory=KeyValueListModel)
    default_key_index: Optional[int] = None

    validation_authority_key: Optional[gpg.Key] = None

    def __post_init__(self) -> None:
        super().__init__()
        if self.config.offline:
            self.encrypt_verify_dtr = self.transfer_verify_dtr = False
        if self.config.output_dir:
            self.encrypt_output_location = Path(self.config.output_dir)
            self.decrypt_output_location = Path(self.config.output_dir)
        if self.config.compression_level is not None:
            self.encrypt_compression_level = self.config.compression_level
        if self.config.package_name_suffix is not None:
            self.encrypt_package_name_suffix = self.config.package_name_suffix
        self.transfer_verify_package_name = self.config.verify_package_name
