#ifndef SHOW_FILE_H
#define SHOW_FILE_H

#include <QMainWindow>

namespace Ui {
class show_file;
}

class show_file : public QMainWindow
{
    Q_OBJECT

public:
    explicit show_file(QWidget *parent = 0);
    ~show_file();

private:
    Ui::show_file *ui;

private slots:
    void updatecontent(void);
};

#endif // SHOW_FILE_H
