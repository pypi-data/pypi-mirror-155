#pragma once
#ifndef BINARY_C_PYTHON_H
#define BINARY_C_PYTHON_H

/*
 * Include binary_C's API
 */
#include "binary_c.h"

/* Binary_c's python API prototypes */
int run_system(char * argstring,
               long int custom_logging_func_memaddr,
               struct libbinary_c_store_t * store,
               struct persistent_data_t * persistent_data,
               int write_logfile,
               int population,
               char ** const buffer,
               char ** const error_buffer,
               size_t * const nbytes);

/* =================================================================== */
/* Functions to call other API functionality like help and arglines    */
/* =================================================================== */

int return_arglines(char ** const outstring,
                char ** const errorstring,
                size_t * const nbytes);

int return_help_info(char * argstring,
                char ** const outstring,
                char ** const errorstring,
                size_t * const nbytes);

int return_help_all_info(char ** const outstring,
                char ** const errorstring,
                size_t * const nbytes);

int return_version_info(char ** const outstring,
                char ** const errorstring,
                size_t * const nbytes);


int return_minimum_orbit_for_RLOF(char * argstring,
                                   struct libbinary_c_store_t * store,
                                    char ** const buffer,
                                    char ** const error_buffer,
                                    size_t * const nbytes);

int return_maximum_mass_ratio_for_RLOF(char * argstring,
                                   struct libbinary_c_store_t * store,
                                   char ** buffer,
                                   char ** error_buffer,
                                   size_t * nbytes);

/* =================================================================== */
/* Functions to handle memory                                          */
/* =================================================================== */

struct libbinary_c_store_t * return_store_memaddr(char ** const buffer,
               char ** const error_buffer,
               size_t * const nbytes);

struct persistent_data_t * return_persistent_data_memaddr(char ** const buffer,
               char ** const error_buffer,
               size_t * const nbytes);

int free_store_memaddr(struct libbinary_c_store_t * store,
               char ** const buffer,
               char ** const error_buffer,
               size_t * const nbytes);

int free_persistent_data_memaddr_and_return_json_output(struct persistent_data_t * persistent_data,
               char ** const buffer,
               char ** const error_buffer,
               size_t * const nbytes);


/* C macros */
#define BINARY_C_APITEST_VERSION 0.1
#define APIprint(...) APIprintf(__VA_ARGS__);
#define NO_OUTPUT

#ifdef BINARY_C_PYTHON_DEBUG
  #define debug_printf(fmt, ...)  printf(fmt, ##__VA_ARGS__);
#else
  #define debug_printf(fmt, ...)    /* Do nothing */
#endif

#endif // BINARY_C_C_PYTHON_H
