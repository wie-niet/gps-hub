
export interface iDeviceHardware {
    readonly id: string;
    readonly ID_FS_UUID?: string;
    readonly ID_FS_LABEL?: string;
    readonly ID_VENDOR?: string;
    readonly ID_FS_TYPE?: string;
    readonly ID_FS_USAGE?: string;
    readonly ID_FS_VERSION?: string;
    readonly ID_SERIAL_SHORT?: string;
    sys_is_mounted: boolean;
    readonly sys_is_connected: boolean;
    readonly sys_mountpoint: string;
    readonly sys_dev_path: string;

}

export interface iDeviceConfig {
    readonly id: string;
    label: string|null;
    gpx_dir: string;
    has_gpx_archive_dir: boolean;
	has_gpx_dir: boolean;
    gpx_archive_dir?: string;
    gpx_dir_hidden_list: Array<string>;
    gpx_dir_readonly_list: Array<string>;
    auto_mount: boolean;
}

export interface iGpxFile {
    file_name: string;
    gpx_name?: string;
    readonly read_only: boolean;
    readonly gpx_data_path: string;


}