import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { NgWhiteboardService } from 'ng-whiteboard';
import { environment } from 'src/environments/environment';
import { CanvasWhiteboardComponent } from 'ng2-canvas-whiteboard';

@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
  viewProviders: [CanvasWhiteboardComponent],
  styleUrls: ['./main.component.scss'],
})
export class MainComponent implements OnInit {
  imagePath = '';
  imgURL: any = '';
  message: any;

  @ViewChild('canvasWhiteboard') canvasWhiteboard: CanvasWhiteboardComponent | undefined;

  constructor(
    public http: HttpClient,
    private whiteboardService: NgWhiteboardService
  ) {}

  ngOnInit(): void {}

  preview(files: any) {
    if (files.length === 0) return;
    var mimeType = files[0].type;
    if (mimeType.match(/image\/*/) == null) {
      this.message = 'Only images are supported.';
      return;
    }

    var reader = new FileReader();
    this.imagePath = files;
    reader.readAsDataURL(files[0]);
    reader.onload = (_event) => {
      this.imgURL = reader.result;
    };
  }

  predictSolution(url: any) {
    console.log(url);
    url = url.split(',');
    const formData = new FormData();
    formData.append('predict', url[1]);
    this.http
      .post(environment.baseURL + 'predict', formData)
      .subscribe((res) => {
        console.log(res);
      });
  }

  onSave(event: any): any {
    let generatedString = this.canvasWhiteboard?.generateCanvasDataUrl("image/jpeg", 0.3);
    console.log(generatedString);
    this.predictSolution(generatedString);
  }


}
