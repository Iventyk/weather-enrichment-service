import { CommonModule } from '@angular/common';
import { Component, EventEmitter, Input, Output, inject } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';

@Component({
  selector: 'app-city-form',
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './city-form.component.html',
  styleUrl: './city-form.component.css',
})
export class CityFormComponent {
  @Input({ required: true }) isSubmitting = false;
  @Output() cityAdded = new EventEmitter<string>();

  private readonly formBuilder = inject(FormBuilder);

  protected readonly form = this.formBuilder.nonNullable.group({
    name: ['', [Validators.required, Validators.maxLength(120)]],
  });

  protected submit(): void {
    if (this.form.invalid || this.isSubmitting) {
      this.form.markAllAsTouched();
      return;
    }

    const cityName = this.form.controls.name.value.trim();
    if (!cityName) {
      this.form.controls.name.setErrors({ required: true });
      return;
    }

    this.cityAdded.emit(cityName);
    this.form.reset();
  }
}
