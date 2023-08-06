from tensorflow import keras
from pyhectiqlab import Run

class KerasCallback(keras.callbacks.Callback):
    
    def __init__(self, run: Run, 
                    level: str= "batch", 
                    exclude_train_metrics: bool = False,
                    exclude_val_metrics: bool = False,
                    exclude_predict_metrics: bool = False,
                    exclude_metrics=[]):
        """
        Keras callback to push the metrics in Hectiq Lab.

        level: "batch" or "epoch". Use epoch to track only the metics each epoch (the stepstamp will be the epoch number.)
        exclude_metrics: List the metrics to remove from tracking. For validation metrics, add "val_". For
            instance, use `exclude_metrics=["mse", "val_mse"]` to exclude the `mse` metrics in training and validation.

        Example usage:
        --------------
            model.fit(
                x_train,
                y_train,
                callbacks=[KerasCallback(run=run)],
            )
        """
        assert level in ["batch", "epoch"]
        self.level = level
        self.exclude_train_metrics = exclude_train_metrics
        self.exclude_val_metrics = exclude_val_metrics
        self.exclude_predict_metrics = exclude_predict_metrics
        self.exclude_metrics = exclude_metrics
        self._run = run
        self.epoch = 0
        self.global_step = 0
    
    def on_train_begin(self, logs=None):
        self._run.training()

    def on_train_end(self, logs=None):
        self._run.completed()

    def on_test_begin(self, logs=None):
        pass

    def on_test_end(self, logs=None):
        if self.level=="epoch":
            return

        if logs is None:
            return

        if self.exclude_val_metrics:
            return

        for metric in logs.keys():
            value = logs[metric]
            if metric in self.exclude_metrics:
                continue
            self._run.add_metrics(f"val_{metric}", step=self.global_step, value=value)

    def on_predict_begin(self, logs=None):
        pass

    def on_predict_end(self, logs=None):
        if logs is None:
            return

        if self.exclude_predict_metrics:
            return

        for metric in logs.keys():
            value = logs[metric]
            if metric in self.exclude_metrics:
                continue
                
            self._run.add_metrics(f"predict_{metric}", step=self.global_step, value=value)

    def on_train_batch_begin(self, batch, logs=None):
        pass

    def on_train_batch_end(self, batch, logs=None):
        self.global_step += 1
        
        if self.level=="epoch":
            return

        if logs == None:
            return

        if self.exclude_train_metrics:
            return

        for metric in logs.keys():
            value = logs[metric]
            if metric in self.exclude_metrics:
                continue
            self._run.add_metrics(f"train_{metric}", step=self.global_step, value=value)

    def on_test_batch_begin(self, batch, logs=None):
        pass

    def on_test_batch_end(self, batch, logs=None):
        pass

    def on_predict_batch_begin(self, batch, logs=None):
        pass

    def on_predict_batch_end(self, batch, logs=None):
        pass

    def on_epoch_begin(self, epoch, logs=None):
        self.epoch = epoch

    def on_epoch_end(self, epoch, logs=None):

        if self.level=="batch":
            return

        for metric in logs.keys():
            value = logs[metric]
            if metric in self.exclude_metrics:
                continue
            if metric.startswith("val_"):
                if self.exclude_val_metrics:
                    continue
            else:
                if self.exclude_train_metrics:
                    continue
            self._run.add_metrics(metric, step=epoch, value=value)

        self.epoch = epoch+1

