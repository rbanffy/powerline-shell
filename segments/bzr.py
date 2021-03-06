import os
import subprocess

def get_bzr_status():
    has_modified_files = False
    has_untracked_files = False
    has_missing_files = False

    p = subprocess.Popen(['bzr', 'status', '--short'], stdout=subprocess.PIPE)
    output = p.communicate()[0]

    for line in output.split('\n'):
        if line == '':
            continue
        elif line[0] == '?':
            has_untracked_files = True
        elif line[1] == 'D':
            has_missing_files = True
        else:
            has_modified_files = True
    return has_modified_files, has_untracked_files, has_missing_files

def add_bzr_segment():
    p1 = subprocess.Popen(['bzr', 'log', '-r-1'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p2 = subprocess.Popen(['grep', 'revno:'], stdin=p1.stdout, stdout=subprocess.PIPE)
    revno = p2.communicate()[0].split(':')[-1].strip()
    if len(revno) == 0:
        return False
    p3 = subprocess.Popen(['bzr', 'info'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p4 = subprocess.Popen(['grep', 'push branch:'], stdin=p3.stdout, stdout=subprocess.PIPE)
    branch_line = p4.communicate()[0].split('/')
    if len(branch_line) != 2:
        branch = ''
    else:
        branch = branch_line[-2].strip()
    bg = Color.REPO_CLEAN_BG
    fg = Color.REPO_CLEAN_FG
    has_modified_files, has_untracked_files, has_missing_files = get_bzr_status()
    if has_modified_files or has_untracked_files or has_missing_files:
        bg = Color.REPO_DIRTY_BG
        fg = Color.REPO_DIRTY_FG
        extra = ''
        if has_untracked_files:
            extra += '+'
        if has_missing_files:
            extra += '!'
        revno += (' ' + extra if extra != '' else '')
    return powerline.append('%s ' % ' '.join([branch, revno]), fg, bg)
