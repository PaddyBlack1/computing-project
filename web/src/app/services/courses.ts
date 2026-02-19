import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

export type CourseSummary = {
  _id: string;
  external_id?: number;
  club_name?: string;
  course_name?: string;
  location?: { city?: string; country?: string; address?: string };
};

@Injectable({ providedIn: 'root' })
export class CoursesService {
  constructor(private http: HttpClient) {}

  getCourses(pn = 1, ps = 12) {
    return this.http.get<any>(`/api/v1.0/courses?pn=${pn}&ps=${ps}`);
  }
}
