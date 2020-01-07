import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { Observable } from 'rxjs';
import { catchError } from 'rxjs/operators';

import { iDeviceHardware, iDeviceConfig, iGpxFile } from '../shared/interfaces';

// export class DeviceHardwareData {
//   readonly ID_FS_UUID: string;
//   readonly ID_FS_LABEL?: string;
//   readonly ID_VENDOR?: string;
//   readonly ID_FS_TYPE?: string;
//   readonly ID_FS_USAGE?: string;
//   readonly ID_FS_VERSION?: string;
//   readonly ID_SERIAL_SHORT?: string;
//   private _sys_is_mounted: boolean;
//   readonly sys_is_connected: boolean;
//   readonly sys_mountpoint: string;
//   readonly sys_dev_path: string;

//   private _meta_is_dirty: boolean;

//   get sys_is_mounted(): boolean {
//     // console.log('getter DeviceHardwareData.get()');
//     return this._sys_is_mounted;
//   }

//   set sys_is_mounted(sys_is_mounted: boolean) {
//     this._meta_is_dirty = true;
//     this._sys_is_mounted = sys_is_mounted;
//     console.log('setter DeviceHardwareData.set('+String(sys_is_mounted)+')')
//   }

//   constructor(item) {
//     this.init_data(item)
//   }

//   private init_data(item) {
//     for (const key in item) {
//       this[key] = item[key];
//     }
//     this._meta_is_dirty = false;
//   }

//   toJsonString(): string {
//     let json = JSON.stringify(this);
//     Object.keys(this).filter(key => key[0] === "_").forEach(key => {
//         json = json.replace(key, key.substring(1));
//     });

//     return json;
//   }

// }



export class RestItem {

}

@Injectable({
  providedIn: 'root'
})
export class DataService {
  // api_url = 'assets/json-data'
  // api_device_hardware_list  = '/DeviceHardware/all.json'
  // api_device_hardware  = '/DeviceHardware/'

  // api_url = 'http://127.0.0.1:5000'
  // api_device_hardware_list  = '/gps-config/'
  // api_device_hardware  = '/gps-config/'
  api_url = 'http://192.168.2.17:5000/api'
  api_device_hardware  = '/gps_dev/'
  api_device_hardware_list  = this.api_device_hardware
  api_device_config = '/gps_conf/'
  
  
  constructor(private http: HttpClient) { }

  getDeviceConfigList(): Observable<iDeviceConfig[]> {
    return this.http.get<iDeviceConfig[]>(this.api_url +  this.api_device_config )
      .pipe(
        catchError(this.handleError)
      );
  }

  getDeviceConfig(id: string): Observable<iDeviceConfig > {
      return this.http.get<iDeviceConfig>(this.api_url + this.api_device_config + id)
      .pipe(
        catchError(this.handleError)
      );
  }

  updateDeviceConfig(dev_conf: iDeviceConfig): Observable<iDeviceConfig > {
    return this.http.put<iDeviceConfig>(this.api_url + this.api_device_config + dev_conf.id, dev_conf)
    .pipe(
      catchError(this.handleError)
    );
  }

  deleteDeviceConfig(id: string): Observable<iDeviceConfig > {
    return this.http.delete<iDeviceConfig>(this.api_url + this.api_device_config + id)
    .pipe(
      catchError(this.handleError)
    );
  }

  /*
   * DeviceHardware /gps_dev/
   */
  getDeviceHardwareList(refresh=false): Observable<iDeviceHardware[]> {
    let url_args = ''
    if(refresh) {
      url_args = '?refresh=true'
    }
    return this.http.get<iDeviceHardware[]>(this.api_url +  this.api_device_hardware_list + url_args)
      // .pipe(
      //   catchError(this.handleError)
      // );
  }

  getDeviceHardware(hwid: string): Observable<iDeviceHardware > {
      return this.http.get<iDeviceHardware>(this.api_url + this.api_device_hardware + hwid)
      .pipe(
        catchError(this.handleError)
      );
  }

  updateDeviceHardware(dev_hw: iDeviceHardware): Observable<iDeviceHardware > {
    return this.http.put<iDeviceHardware>(this.api_url + this.api_device_hardware + dev_hw.id, dev_hw)
    .pipe(
      catchError(this.handleError)
    );
  }

  mountDeviceHardware(dev_hw: iDeviceHardware, mount_action: boolean): Observable<iDeviceHardware > {
    let json_patch = [{path: "/sys_is_mounted", op: "replace", value: mount_action}];
    return this.http.patch<iDeviceHardware>(this.api_url + this.api_device_hardware + dev_hw.id, json_patch)
    // .pipe(
    //   catchError(this.handleError)
    // );
  }



  private handleError(error: any) {
    console.error('server error:', error);
    console.log(error);
    // alert(error);
    let msg = "api error: " + error.error.error + "\n" +  error.error.message
	  alert(msg);
    // if (error.error instanceof Error) {
    //     const errMessage = error.error.message;
    //     return Observable.throw(errMessage);
    // }
	throw new Error(error.error.message);
    
    return Observable.throw(error || 'Server error');
  }

}
