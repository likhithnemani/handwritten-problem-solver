import {
  AfterViewInit,
  Component,
  ElementRef,
  OnInit,
  ViewChild,
} from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { CommonService } from '../common.service';
import { environment } from 'src/environments/environment';
import { CanvasWhiteboardComponent } from 'ng2-canvas-whiteboard';
import * as bootstrap from 'bootstrap';
import { Modal } from 'bootstrap';

@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
  viewProviders: [CanvasWhiteboardComponent],
  styleUrls: ['./main.component.scss'],
})
export class MainComponent implements OnInit, AfterViewInit {
  load = false;
  imagePath = '';
  imgURL: any = '';
  message: any;

  predictedValue = {
    solution: '',
    equation: '',
  };

  modalRef: any;

  @ViewChild('canvasWhiteboard') canvasWhiteboard:
    | CanvasWhiteboardComponent
    | undefined;
  @ViewChild('myModal') myModal: ElementRef<HTMLElement> | undefined;

  constructor(
    public http: HttpClient,
    public elementRef: ElementRef,
    public commonService: CommonService
  ) {}

  ngOnInit(): void {}

  ngAfterViewInit(): void {
    if (this.myModal) {
      this.modalRef = new Modal(this.myModal.nativeElement);
    }
  }

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
    this.load = true;
    console.log(url);
    url = url.split(',');
    const formData = new FormData();
    formData.append('predict', url[1]);
    this.http.post(environment.baseURL + 'predict', formData).subscribe(
      (res) => {
        console.log(res);
        let s: string = JSON.stringify(res) || '';
        let x = JSON.parse(s);
        this.predictedValue.equation = x.equation;
        this.predictedValue.solution = x.solution;
        this.modalRef.toggle();
        this.load = false;
      },
      (err) => {
        console.log(err);
        this.load = false;
      }
    );
  }

  onSave(event: any): any {
    let generatedString = this.canvasWhiteboard?.generateCanvasDataUrl(
      'image/jpeg',
      0.3
    );
    console.log(generatedString);
    this.predictSolution(generatedString);
  }

  copyToClipboard(item: any) {
    navigator.clipboard.writeText(item).then().catch(e => console.error(e));
  }
}
